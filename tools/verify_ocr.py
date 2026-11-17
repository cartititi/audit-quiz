#!/usr/bin/env python3
"""전사 결과를 macOS Vision OCR 결과와 양방향으로 대조해 의심 구간만 출력한다.

1) OCR 텍스트 만들기 (사진 폴더 → txt 폴더):
   swiftc -O tools/vision_ocr.swift -o /tmp/vocr
   /tmp/vocr <txt출력폴더> <사진폴더>/*.JPG
2) 대조:
   python3 -I tools/verify_ocr.py <txt출력폴더> [--ch 12,13,14]

출력된 구간은 '의심'일 뿐이다. 기울어진 줄·표 칸을 OCR이 섞어 읽어서 생기는 차이가 대부분이므로
원본 사진을 확대해서 직접 확인한 뒤에만 고친다. 숫자는 따로 전수 대조한다.
"""
import difflib, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'[\s·・•\-－–—~∼〜‘’“”"\'`.,:;()\[\]〈〉<>|│*※]', '', s)


def best(sub, corpus):
    if sub in corpus: return 1.0
    b = 0
    for m in difflib.SequenceMatcher(None, sub, corpus, autojunk=False).get_matching_blocks():
        if m.size < 3: continue
        st = max(0, m.b - m.a - 3)
        b = max(b, difflib.SequenceMatcher(None, sub, corpus[st:st + len(sub) + 6], autojunk=False).ratio())
        if b > .97: break
    return b


def main():
    txtdir = sys.argv[1]
    chs = None
    if '--ch' in sys.argv: chs = {int(x) for x in sys.argv[sys.argv.index('--ch') + 1].split(',')}
    d = json.load(open(os.path.join(ROOT, 'data', 'questions.json'), encoding='utf-8'))
    qs = [q for q in d['questions'] if not chs or q['ch'] in chs]
    tgs = {q['tg'] for q in qs}
    texts = [(q['id'], q['q']) for q in qs] + [(k, v) for k, v in d['ctx'].items() if k in tgs]
    texts += [(q['id'] + ' 해답', q.get('model') or q.get('ex') or '') for q in qs]
    M = norm(' '.join(t for _, t in texts))
    ocr = {os.path.basename(p): open(p, encoding='utf-8').read().split('\n') for p in sorted(glob.glob(os.path.join(txtdir, '*.txt')))}
    O = norm(' '.join(' '.join(v) for v in ocr.values()))
    print('== 1) 원본 OCR 줄 중 전사본에 잘 안 맞는 것 (머리글·OCR 오인식이 대부분)')
    for img, lines in ocr.items():
        for l in lines:
            n = norm(l)
            if len(n) >= 8 and best(n, M) < .8: print(f'  {img}: {l}')
    print('== 2) 전사 구간 중 원본 OCR에 잘 안 맞는 것')
    for key, txt in texts:
        t = re.sub(r'<br\s*/?>|</p>|</td>|</th>|</tr>|\n', ' ¶ ', txt); t = re.sub(r'<[^>]+>', '', t)
        for seg in re.split(r'¶|(?<=다\.)|(?<=\?)|(?<=오\.)', t):
            n = norm(seg)
            if len(n) >= 10 and best(n, O) < .86: print(f'  {key}: {seg.strip()[:90]}')
    print('== 3) 전사본 숫자 중 OCR에 없는 것 (반드시 원본 확대 확인)')
    allt = re.sub(r'<[^>]+>', ' ', ' '.join(t for _, t in texts))
    On = O.replace(' ', '')
    for n in sorted({x for x in re.findall(r'\d[\d,\.]*\d', allt) if len(x) >= 3 and x not in On}):
        print('  ', n)


if __name__ == '__main__':
    main()
