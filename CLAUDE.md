# 회계감사 기말 퀴즈 — 새 범위 추가 작업 지시서

이 폴더에서 작업을 시작하면 이 문서대로 진행한다. 사용자가 "12장 추가해", "○○ 폴더 사진 넣어줘"처럼 말하면 아래 절차 전체를 수행하고 push까지 끝낸다.

## 사용자 원칙 (반드시 지킬 것)
- **원문 그대로 전사.** 요약·의역·맞춤법 교정 금지. 오타처럼 보여도 원본을 확대해 확인한 뒤 그대로 두고 메모에 남긴다.
- **Claude의 독자적 해석·해설 금지.** 정답·해설·모범답안은 사진 속 해답편 문장만 쓴다. 해답이 사진에 없으면 비워 두고 사용자에게 알린다(만들어 넣지 않는다).
- 표는 행/열 구조를 유지한 HTML `<table>`로 옮긴다. 판독 불확실 글자는 `[?]`, 마지막에 불확실 목록 보고.
- 문항마다 원본 파일명 + 교재 쪽수(`src`), 해답 파일명 + 해답편 쪽수(`asrc`)를 기록한다.
- 서술형은 시험에 똑같이 나오므로 "외우기"가 목적이다. 지문은 접지 않고 전부 보여준다(현재 앱이 이미 그렇게 동작).

## 위치
- 작업 폴더: `audit-quiz-main/` (로컬 사본, git 아님)
  - `data/questions.json` — 모든 문항 데이터 (유일한 원본)
  - `tools/app_template.html` — 앱 코드. `__DATA__` 자리에 데이터가 들어감
  - `tools/build.py` — 검증 후 `index.html` 생성
  - `tools/verify_ocr.py`, `tools/vision_ocr.swift` — 원본 재대조용
  - `index.html` — 빌드 결과물 (직접 수정하지 말 것)
- 배포 저장소: GitHub `cartititi/audit-quiz` (gh 로그인 계정 cartititi), `main` 브랜치 루트가 GitHub Pages → https://cartititi.github.io/audit-quiz/
- 사진 폴더: 범위별로 `Audit-quiz/<폴더>/IMG_xxxx.JPG` (기말 1차분은 `기말/`)
- 중간고사 버전은 저장소 커밋 `ad7d3ae`에 보존

## 데이터 형식 (`data/questions.json`)
```
meta.chapters : {"6": "장 제목", ...}   ← 새 장을 넣으면 여기에 장 제목 추가 (홈 필터가 자동으로 생김)
groups        : [{"g": "12-진위", "ch": 12, "name": "12장 진위", "title": "진위형"}, ...]   ← 화면에 나오는 순서
ctx           : {"12-서술①": "<p>지문 HTML</p>", "12-진위": "<p>다음의 설명을 읽고, 틀린 기술이라면 그 이유를 제시하시오.</p>"}
questions     : 문항 배열
uncertain     : [["파일 · 쪽", "설명"], ...]   ← 남은 [?] 항목
notes         : [["파일 · 쪽", "설명"], ...]   ← 원문이 이상해 보여도 그대로 둔 곳 등
```
문항 예시:
```
O/X : {"id":"TB12-TF01","ch":12,"k":"ox","tb":"12장 진위 (1)","tg":"12-진위","cx":"12-진위",
       "q":"문장 원문","a":false,"ex":"해답편 해설 원문(○만 있으면 빈 문자열)",
       "src":"IMG_xxxx.JPG · p.000","asrc":"IMG_yyyy.JPG · 해답 p.00"}
서술 : {"id":"TB12-E1-2","ch":12,"k":"essay","tb":"12장 서술① 2","tg":"12-서술①","cx":"12-서술①",
       "q":"요구사항 2 원문","model":"해답 원문. 줄바꿈은 \n, 표는 <table>…</table>","pts":[],"ex":"",
       "src":"…","asrc":"…"}
```
- id 규칙: 진위 `TB{장}-TF{두자리}`, 서술 `TB{장}-E{문제번호}-{요구사항번호}`, 사례연구 `TB{장}-C1-{번호}`
- 그룹 키: `{장}-진위`, `{장}-서술①…`, `{장}-사례`. 제목 옆 출처 표기 (KICPA)/(AICPA)는 group title 끝에 붙인다.
- 요구사항이 여러 개면 요구사항마다 문항 1개. 공통 지문은 ctx에 넣고 각 문항 `cx`로 연결.
- 해답이 표 한 장(열 1·2·3 = 요구사항 1·2·3)이면 열별로 나눠 각 문항 model에 넣고 asrc에 "(표 n열)"을 적는다.

## 절차
1. **사진 확인**: 폴더의 JPG 개수와 번호 확인. 빠진 번호가 있으면 앞뒤 쪽수가 이어지는지 보고 메모.
2. **읽기용 축소본**: 스크래치패드에 `sips -Z 2000`으로 줄여서 Read로 본다. 원본은 EXIF 회전이 있으므로 확대 크롭은 PIL `ImageOps.exif_transpose` 후 원본 해상도로 한다.
3. **10장씩 처리**: 문제 쪽 → 해답 쪽 순서로 전사. 배치마다 사용자에게 "처리한 파일 · 쪽 · 새 문항 수 · 해답 연결 수"를 한 줄씩 보고한다.
   - 사진이 기울어 줄이 섞여 보이면 줄의 왼쪽 시작과 오른쪽 끝을 짝지어 원래 줄을 복원한다. 애매하면 원본 크롭으로 확인.
   - 진위형 지시문, 요구사항 머리말("다음 각 물음에 대해 답하시오." 등)도 빠뜨리지 말 것(1차분에서 빠졌던 부분).
4. **데이터 병합**: `data/questions.json`에 groups·ctx·questions·meta.chapters 추가. 기존 문항은 건드리지 않는다.
5. **재대조**(사용자 요구사항): 
   ```
   swiftc -O -sdk /Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk tools/vision_ocr.swift -o <scratchpad>/vocr
   <scratchpad>/vocr <scratchpad>/vision <축소본폴더>/*.JPG
   python3 -I tools/verify_ocr.py <scratchpad>/vision --ch 12,13,14
   ```
   (`-sdk` 없이 하면 "SDK is not supported by the compiler" 오류: 기본 SDK(27)가 컴파일러보다 새것이라서. OCR을 전사 전에 미리 돌려 두면 초안 대조용으로도 쓸 수 있다.)
   나온 구간은 '의심'일 뿐이다(대부분 머리글·OCR 오인식). 원본을 확대해서 확인하고 **실제 불일치만** 고친 뒤 목록으로 보고한다. 숫자 목록은 하나씩 원본 확대로 확인(1차분에서는 OCR이 틀리고 전사가 맞았다).
6. **빌드**: `cd audit-quiz-main && python3 -I tools/build.py` (검증 실패 시 메시지대로 고친다). 앱 코드를 고쳤다면 `node --check`로 스크립트 문법 확인, 헤드리스 크롬으로 화면 확인(헤드리스 최소 폭이 500px이라 휴대폰 폭은 375px iframe에 넣어 스크린샷).
7. **배포**: `gh repo clone cartititi/audit-quiz <scratchpad>/repo` → `index.html`, `data/`, `tools/`, `CLAUDE.md`를 복사 → 커밋(메시지 끝에 Co-Authored-By 줄) → `git push origin main` → `gh api repos/cartititi/audit-quiz/pages/builds/latest`가 `built`가 될 때까지 확인.
8. **최종 보고**: 장별 문항 수, 해답 없는 문항, `[?]` 목록, 재대조 불일치 목록, 원문 그대로 둔 곳.

## 보류 문항
- 해답 사진이 없으면 문항을 만들지 말고 `data/pending.json`(questions.json과 같은 형식 + 문항별 `pending` 사유, 남은 쪽에 보이는 해답 일부 `partial`, O/X는 `a`=null)에 따로 두었다가, 사진을 받으면 model·asrc를 채우고 questions.json으로 옮긴다. 빌드 검증은 questions.json만 본다. (2차분은 모두 해결되어 현재 pending.json 없음)

## 현재 상태 (2026-11-24)
- 수록: 6·7·9장(1차) + 12~16장(2차) → 276문항, 전부 해답 연결. 12장 23, 13장 23, 14장 39, 15장 47, 16장 41
- `기말2(12~끝)`의 "JPEG 이미지-…jpeg" 9개는 빈 파일(복사 실패)이었고, 해당 사진 9장(IMG_7853·7854·7856·7859·7861~7864·7866)은 `추가/` 폴더로 다시 받아 모두 반영. 해답편 p.121–122는 문항 해답 없음
- 출처 사진: `기말/IMG_7610~7656`, `기말2(12~끝)/IMG_7793~7870`, `추가/IMG_7853~7866 중 9장` (문제 p.553–733, 해답 p.102–137 연속)
- verify_ocr.py 수정(2026-11-24): OCR 텍스트에 태그 제거 정규식을 적용해 짝 안 맞는 '<' 뒤가 통째로 지워지던 문제, 숫자 비교 때 쉼표 때문에 모든 숫자가 '없음'으로 나오던 문제
- 원문 그대로 둔 곳: 6장 사례연구 "감사계약을 제한하며", 7장 서술③ 해답 "(2) 급여이체명세서를 감독관에게 보내지 않고 있다" (data의 notes에 기록됨)
