#!/usr/bin/env python3
"""data/questions.json 을 검증한 뒤 tools/app_template.html 에 넣어 index.html 을 만든다.

사용: python3 -I tools/build.py        (저장소 루트에서)
검증에 실패하면 index.html 을 건드리지 않고 종료한다.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'questions.json')
TPL = os.path.join(ROOT, 'tools', 'app_template.html')
OUT = os.path.join(ROOT, 'index.html')


def validate(d):
    err = []
    groups = {g['g']: g for g in d['groups']}
    seen = set()
    for q in d['questions']:
        i = q.get('id', '?')
        if i in seen: err.append(f'{i}: id 중복')
        seen.add(i)
        for f in ('ch', 'k', 'tb', 'tg', 'q', 'src', 'asrc'):
            if not q.get(f) and q.get(f) != 0: err.append(f'{i}: {f} 비어 있음')
        if q.get('tg') not in groups: err.append(f'{i}: tg {q.get("tg")} 가 groups 에 없음')
        if q['k'] == 'ox':
            if not isinstance(q.get('a'), bool): err.append(f'{i}: ox 인데 a 가 true/false 가 아님')
        elif q['k'] == 'essay':
            if not q.get('model'): err.append(f'{i}: essay 인데 model(해답) 비어 있음')
            if q.get('cx') and q['cx'] not in d['ctx']: err.append(f'{i}: cx {q["cx"]} 가 ctx 에 없음')
        else:
            err.append(f'{i}: k 는 ox 또는 essay 만 지원')
        if str(q['ch']) not in d['meta'].get('chapters', {}): err.append(f'{i}: meta.chapters 에 {q["ch"]}장 이름 없음')
    for g in d['groups']:
        if not any(q['tg'] == g['g'] for q in d['questions']): err.append(f'group {g["g"]}: 문항 없음')
    return err


def main():
    d = json.load(open(DATA, encoding='utf-8'))
    err = validate(d)
    if err:
        print('검증 실패:'); [print(' -', e) for e in err]; sys.exit(1)
    d['meta']['count'] = len(d['questions'])
    json.dump(d, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    s = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    tpl = open(TPL, encoding='utf-8').read()
    assert '__DATA__' in tpl
    open(OUT, 'w', encoding='utf-8').write(tpl.replace('__DATA__', s))
    from collections import Counter
    c = Counter((q['ch'], q['k']) for q in d['questions'])
    print(f"index.html 생성 · 총 {len(d['questions'])}문항 · " + ', '.join(f'{ch}장 {k} {n}' for (ch, k), n in sorted(c.items())))


if __name__ == '__main__':
    main()
