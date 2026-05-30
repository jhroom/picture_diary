# Day 2 self1: scene_draft.md 4장면 초안 작성 — 실습가이드 (60분)

Block self-B 시작 (1/2)  
산출 파일: `scene_draft.md`, `day2_self1.py`(검증 스크립트), `dev_log.md`(이어쓰기)  
핵심 키워드: 샷·앵글·조명·구도·렌즈, 4장면 일관성

---

## 세션 개요

오늘은 Day 1 self2에서 만든 `scene_draft_seed.md`를 바탕으로 그림일기 4장면을 정식 초안으로 정리합니다.

이 세션의 목적은 이미지를 바로 생성하는 것이 아닙니다.  
Day 2 self2에서 사용할 장면 설계 문서를 먼저 단단하게 만드는 시간입니다.

- 오늘은 API를 호출하지 않습니다.
- 오늘은 이미지 파일을 만들지 않습니다.
- 오늘은 `scene_draft.md`와 `day2_self1.py`만 만듭니다.

`scene_draft.md`에는 4개의 장면이 들어갑니다.  
각 장면에는 한국어 장면 설명과 시각 어휘가 들어갑니다.  
시각 어휘는 강사 시간에 배운 다섯 묶음을 사용합니다.

- shot: WS, MS, BS, CU, ECU
- angle: eye-level, low, high
- light: soft, rim, backlit
- composition: rule of thirds, symmetric, leading line
- lens: 24mm, 35mm, 50mm, 85mm

이 다섯 묶음은 그림일기 장면을 이미지 생성 프롬프트로 바꿀 때 뼈대가 됩니다.  
영문 프롬프트는 길게 쓰지 않아도 됩니다. 단, 장면 설명과 시각 어휘가 한 줄 안에 들어가야 합니다.

오늘의 작업 흐름은 아래 순서입니다.

1. seed 파일을 확인합니다.
2. 그릴 장면 4개를 고릅니다.
3. 각 장면에 샷·앵글·조명·구도·렌즈를 붙입니다.
4. `day2_self1.py` 검증 스크립트의 빈칸을 채웁니다.
5. 실행 결과를 보고 빠진 필드를 고칩니다.
6. `dev_log.md`에 오늘 결정과 막힌 점을 적습니다.

오늘의 산출 위치는 `picture_diary/` 폴더입니다.  
터미널에서 먼저 작업 위치를 확인합니다.

```bash
cd picture_diary
pwd
ls
```

`scene_draft_seed.md`가 보이면 시작할 수 있습니다.

---

## 1. scene_draft_seed.md 확인 (5분)

🎯 **학생 행동**: Day 1 self2에서 만든 장면 후보 메모를 열어, 오늘 사용할 장면 후보가 3~5개 있는지 확인합니다.

먼저 현재 폴더에 어떤 파일이 있는지 봅니다.

```bash
ls
```

다음 파일이 보여야 합니다.

```
scene_draft_seed.md
```

파일이 보이면 아래 코드를 Python REPL 또는 임시 셀에서 실행합니다.

```python
from pathlib import Path
seed = Path("scene_draft_seed.md")
if seed.exists():
    print(seed.read_text(encoding="utf-8")[:500])
else:
    print("scene_draft_seed.md 없음 — Day 1 self2 산출물을 확인하세요.")
```

화면에 후보 장면이 보이면 이어서 읽습니다.  
장면 후보는 완벽한 문장이 아니어도 괜찮습니다. 아래처럼 짧은 메모여도 됩니다.

```
- 아침에 늦게 일어나 창밖을 봄
- 버스 정류장까지 뛰어감
- 친구를 만나 웃음
- 집에 돌아와 일기를 씀
```

중요한 것은 장면이 그림으로 보이는지입니다.  
아래 기준으로 후보를 표시해 봅니다.

- 사람이 보이는가
- 장소가 보이는가
- 행동이 보이는가
- 시간이나 분위기가 보이는가
- 한 장의 그림으로 그릴 수 있는가

후보가 3개뿐이면 하나를 더 나누어 4장면으로 만듭니다.  
예를 들어 "비 오는 길을 걷고 집에 옴"은 두 장면으로 나눌 수 있습니다.

- 비 오는 길을 걷는 장면
- 집 문 앞에 도착한 장면

후보가 5개 이상이면 가장 중요한 4개만 고릅니다.  
4장면은 하루의 흐름이 보이도록 배열합니다. 보통은 아래 순서가 편합니다.

1. 시작 장면
2. 이동 또는 변화 장면
3. 사건 또는 감정 변화 장면
4. 마무리 장면

작업 중 seed 파일은 지우지 않습니다. 오늘 새로 만드는 파일은 `scene_draft.md`입니다.

---

## 2. 4장면 선정 + 시각 어휘 표 작성 (15분)

🎯 **학생 행동**: seed 파일에서 4장면을 고르고, 각 장면에 shot, angle, light, composition, lens를 붙여 `scene_draft.md`를 작성합니다.

먼저 빈 파일을 만듭니다.

```bash
touch scene_draft.md
```

편집기에서 `scene_draft.md`를 엽니다. 아래 양식을 그대로 넣고 괄호 안을 채웁니다.

```markdown
# scene_draft.md — 그림일기 4장면 초안

## 장면 1
- scene_kr: (한 줄 설명)
- shot: (WS|MS|BS|CU|ECU)
- angle: (eye-level|low|high)
- light: (soft|rim|backlit)
- composition: (rule of thirds|symmetric|leading line)
- lens: (24mm|35mm|50mm|85mm)
- prompt_en: (영문 1줄 — 위 어휘 결합)

## 장면 2
(동일 구조)

## 장면 3
(동일 구조)

## 장면 4
(동일 구조)
```

각 필드의 역할은 아래와 같습니다.

| 필드 | 쓰는 내용 |
|---|---|
| scene_kr | 한국어 한 줄 장면 설명 |
| shot | 인물이나 배경이 얼마나 크게 보이는지 |
| angle | 카메라가 어느 높이에서 보는지 |
| light | 빛의 느낌과 방향 |
| composition | 화면 안에서 대상을 배치하는 방식 |
| lens | 공간감과 배경 흐림을 정하는 렌즈 느낌 |
| prompt_en | 위 정보를 합친 영어 한 줄 |

shot은 아래 기준으로 고릅니다.

| shot | 장면 느낌 |
|---|---|
| WS | 배경과 인물이 함께 보임 |
| MS | 상반신 또는 허리 위가 보임 |
| BS | 가슴 위 중심의 인물 장면 |
| CU | 얼굴, 손, 물건을 가깝게 보여 줌 |
| ECU | 눈, 손끝, 물방울처럼 아주 가까움 |

angle은 아래 기준으로 고릅니다.

| angle | 장면 느낌 |
|---|---|
| eye-level | 평범하고 자연스러운 시선 |
| low | 대상을 크게 보이게 하는 낮은 시선 |
| high | 위에서 내려다보는 시선 |

light는 아래 기준으로 고릅니다.

| light | 장면 느낌 |
|---|---|
| soft | 부드럽고 안정적인 빛 |
| rim | 인물 윤곽을 강조하는 빛 |
| backlit | 뒤에서 비추어 실루엣이 생기는 빛 |

composition은 아래 기준으로 고릅니다.

| composition | 장면 느낌 |
|---|---|
| rule of thirds | 화면을 3등분해 자연스럽게 배치 |
| symmetric | 좌우 균형이 강한 정돈된 화면 |
| leading line | 길, 복도, 창틀처럼 시선을 이끄는 선 |

lens는 아래 기준으로 고릅니다.

| lens | 장면 느낌 |
|---|---|
| 24mm | 넓은 공간, 배경 강조 |
| 35mm | 거리감이 자연스러운 장면 |
| 50mm | 사람 눈에 가까운 안정감 |
| 85mm | 인물이나 물건을 부드럽게 강조 |

4장면을 고를 때 모든 장면을 같은 방식으로 만들 필요는 없습니다.  
오히려 장면마다 거리감이 달라야 그림일기가 단조롭지 않습니다.  
예를 들어 아래처럼 섞어 봅니다.

- 장면 1: WS로 장소 소개
- 장면 2: MS로 행동 보여 주기
- 장면 3: BS 또는 CU로 감정 보여 주기
- 장면 4: CU로 기억에 남는 물건 보여 주기

`prompt_en`은 영어 문법보다 키워드 연결이 중요합니다.  
다음 순서를 사용하면 쉽습니다.

```
주인공/대상 + 행동/장소 + shot + angle + light + composition + lens + mood
```

예를 들어 본인의 장면이 "학교 복도에서 친구를 기다림"이라면 아래처럼 시작할 수 있습니다.

```
student waiting in school hallway, medium shot, eye-level, soft light, leading line, 35mm, quiet mood
```

위 문장을 그대로 쓰지 말고 자신의 장면에 맞게 바꿉니다.  
오늘은 완성된 영어 문장보다 빠지지 않은 정보가 더 중요합니다.

다음 점검을 하며 4장면을 정리합니다.

- 장면 1~4가 시간 순서로 이어지는가
- 각 장면이 한 장의 그림으로 보이는가
- scene_kr가 너무 추상적이지 않은가
- prompt_en에 shot, angle, light, composition, lens가 들어갔는가
- 같은 shot만 반복하지 않았는가
- 렌즈가 장면 목적과 어울리는가

작성 중 막히면 아래 선택표를 사용합니다.

| 하고 싶은 표현 | 추천 조합 |
|---|---|
| 하루가 시작되는 장소 소개 | WS, eye-level, soft, rule of thirds, 24mm |
| 길을 걷거나 이동하는 장면 | WS, low, rim, leading line, 24mm |
| 친구와 대화하는 장면 | MS, eye-level, soft, symmetric, 35mm |
| 감정이 드러나는 표정 | BS, eye-level, soft, rule of thirds, 50mm |
| 손에 든 물건 강조 | CU, high, soft, rule of thirds, 85mm |
| 비나 빛의 분위기 강조 | MS, low, backlit, leading line, 35mm |

`scene_draft.md` 저장 후 터미널에서 확인합니다.

```bash
cat scene_draft.md
```

장면 헤딩은 반드시 아래 형식을 유지합니다.

```
## 장면 1
## 장면 2
## 장면 3
## 장면 4
```

숫자 앞뒤에 다른 말을 붙이지 않습니다. 검증 스크립트가 이 형식을 기준으로 장면 수를 셉니다.

---

## 3. day2_self1.py 검증 스크립트 함수 골격 (15분)

🎯 **학생 행동**: `scene_draft.md`가 4장면과 7필드를 갖추었는지 확인하는 Python 파일을 만들고, 표시된 빈칸을 채웁니다.

오늘 스크립트는 이미지를 만들지 않습니다. 파일을 읽고 필드가 있는지만 확인합니다.

새 파일을 만듭니다.

```bash
touch day2_self1.py
```

아래 코드를 넣습니다. 표시된 주석이 있는 줄을 중심으로 직접 채웁니다.

```python
# day2_self1.py — scene_draft.md 4장면 필드 검증
from pathlib import Path
import re

REQUIRED_FIELDS = ["scene_kr", "shot", "angle", "light", "composition", "lens", "prompt_en"]

def load_draft(path: Path) -> str:
    """scene_draft.md를 읽어 본문을 반환."""
    # 여기에 path.read_text(encoding='utf-8') 반환 코드를 채워요.
    return ""

def count_scenes(text: str) -> int:
    """본문에서 '## 장면 N' 헤딩 수를 카운트."""
    # 여기에 re.findall + 길이 반환 코드를 채워요.
    # 힌트: 정규식 r'^## 장면 \d+' (re.M 플래그).
    return 0

def check_fields(text: str, scene_idx: int) -> list[str]:
    """주어진 장면 인덱스에 빠진 필드 목록 반환. 모두 있으면 빈 리스트."""
    # 여기에 본문에서 '## 장면 {scene_idx}' 섹션을 잘라낸 후
    #   REQUIRED_FIELDS 각각 'field:' 패턴이 있는지 검사하고 누락 목록을 반환하는 코드를 채워요.
    missing: list[str] = []
    return missing

if __name__ == "__main__":
    draft = load_draft(Path("scene_draft.md"))
    n = count_scenes(draft)
    print(f"[검출] 장면 수: {n}")
    # 여기에 1~4 각 장면에 대해 check_fields 호출 + 누락 출력 코드를 채워요.
    print("[완료] 모든 장면 OK이면 self2로 진행하세요.")
```

함수는 세 개입니다.

- `load_draft()`는 파일을 읽습니다.
- `count_scenes()`는 장면 헤딩 개수를 셉니다.
- `check_fields()`는 특정 장면에 7개 필드가 있는지 봅니다.

먼저 `load_draft()`부터 채웁니다. 이 함수는 `Path` 객체를 받아 문자열을 반환해야 합니다.

다음으로 `count_scenes()`를 채웁니다.  
정규식은 줄의 시작에 있는 `## 장면 숫자`를 찾습니다.  
`re.M` 플래그를 쓰면 여러 줄 본문에서도 줄 시작을 인식합니다.

그다음 `check_fields()`를 채웁니다.  
이 함수는 한 장면만 검사해야 합니다. 전체 문서에서 모든 필드를 한꺼번에 찾으면 안 됩니다.  
예를 들어 장면 1에 lens가 없는데 장면 2에 lens가 있으면 장면 1은 여전히 빠진 상태입니다.  
따라서 장면별 섹션을 나눈 뒤 검사해야 합니다.

마지막으로 main 영역을 채웁니다.  
1부터 4까지 반복하며 `check_fields()`를 호출합니다.  
빠진 필드가 없으면 해당 장면을 OK로 표시합니다.  
빠진 필드가 있으면 어떤 필드가 없는지 표시합니다.

코드를 채운 뒤 저장합니다. 아직 실행하지 않고 눈으로 먼저 확인합니다.  
확인할 부분은 아래 네 가지입니다.

- `Path("scene_draft.md")` 파일명이 정확한가
- 함수 이름을 바꾸지 않았는가
- `REQUIRED_FIELDS` 필드명이 `scene_draft.md`와 같은가
- 들여쓰기가 깨지지 않았는가

---

## 4. 실행하고 검증 (5분)

🎯 **학생 행동**: `day2_self1.py`를 실행해 장면 수와 각 장면 필드 상태를 확인하고, 빠진 항목이 있으면 `scene_draft.md`를 고칩니다.

터미널에서 아래 명령을 실행합니다.

```bash
python day2_self1.py
```

잘 채워진 경우 화면은 아래 흐름과 비슷해야 합니다.

```
[검출] 장면 수: 4
장면 1: OK
장면 2: OK
장면 3: OK
장면 4: OK
[완료] 모든 장면 OK이면 self2로 진행하세요.
```

장면 수가 4가 아니면 `scene_draft.md`의 헤딩을 확인합니다.  
아래 형식을 지켜야 합니다.

```
## 장면 1
```

아래처럼 쓰면 카운트가 달라질 수 있습니다.

```
### 장면 1
## 1번 장면
## Scene 1
```

필드가 빠졌다고 나오면 해당 장면만 고칩니다.  
예를 들어 장면 3에 lens가 없으면 장면 3 아래에 `- lens:` 줄을 추가합니다.  
필드 이름은 영어 소문자로 유지합니다. `light`를 `lighting`으로 바꾸지 않습니다. 오늘 파일에서는 `light`를 씁니다.

수정 후 다시 실행합니다.

```bash
python day2_self1.py
```

반복 횟수는 많지 않아도 됩니다. 오늘 목표는 4장면이 모두 구조를 갖추는 것입니다.  
프롬프트 문장을 꾸미는 데 너무 오래 쓰지 않습니다.  
장면이 구조적으로 통과하면 Day 2 self2에서 JSON으로 바꾸며 더 다듬을 수 있습니다.

---

## 5. dev_log.md 이어쓰기 (3분)

🎯 **학생 행동**: 오늘 고른 4장면과 시각 어휘 선택 이유를 `dev_log.md`에 짧게 이어 씁니다.

`dev_log.md`가 이미 있으면 맨 아래에 덧붙입니다. 없으면 새로 만듭니다.

```bash
touch dev_log.md
```

아래 형식을 사용합니다.

```markdown
## Day 2 self1 기록
- 오늘 만든 파일: scene_draft.md, day2_self1.py
- 장면 1:
- 장면 2:
- 장면 3:
- 장면 4:
- 가장 어려웠던 선택:
- 다음 self2에서 확인할 것:
```

장면별로 길게 쓰지 않아도 됩니다. 한 줄씩만 적어도 충분합니다.  
예를 들어 아래처럼 쓸 수 있습니다.

```
장면 1은 장소 소개라서 WS와 24mm를 골랐다.
장면 4는 손에 든 물건을 보여 주고 싶어서 CU와 85mm를 골랐다.
```

오늘 기록은 다음 시간에 장면을 JSON으로 옮길 때 도움을 줍니다.  
왜 그 어휘를 골랐는지 기억나지 않으면 프롬프트가 흔들립니다.  
기록은 짧아도 됩니다. 다만 선택 이유가 하나라도 있어야 합니다.

---

## 6. 자기 점검 (10분)

🎯 **학생 행동**: 파일 2개와 기록 1개를 열어, Day 2 self2로 넘어갈 준비가 되었는지 직접 확인합니다.

아래 항목을 순서대로 체크합니다.

- [ ] `picture_diary/scene_draft.md`가 있다.
- [ ] `picture_diary/day2_self1.py`가 있다.
- [ ] `picture_diary/dev_log.md`에 오늘 기록을 이어 썼다.
- [ ] `scene_draft.md`에 `## 장면 1`부터 `## 장면 4`까지 있다.
- [ ] 각 장면에 `scene_kr`가 있다.
- [ ] 각 장면에 `shot`이 있다.
- [ ] 각 장면에 `angle`이 있다.
- [ ] 각 장면에 `light`가 있다.
- [ ] 각 장면에 `composition`이 있다.
- [ ] 각 장면에 `lens`가 있다.
- [ ] 각 장면에 `prompt_en`이 있다.
- [ ] `prompt_en`은 영어 키워드 중심으로 적었다.
- [ ] `python day2_self1.py` 실행 시 장면 수가 4로 나온다.
- [ ] 장면별 빠진 필드가 없도록 고쳤다.
- [ ] API 키나 개인 비밀번호를 파일에 넣지 않았다.
- [ ] Day 2 self2에서 이어 쓸 장면 순서가 정해졌다.

완성된 `scene_draft.md`는 Day 2 self2에서 `scene_prompts.json`으로 변환하고 fal.ai FLUX 모델로 첫 이미지를 생성합니다.  
다음 세션에서는 오늘 만든 4장면 중 첫 장면만 먼저 호출합니다.  
따라서 오늘은 이미지를 많이 만들려고 하지 않습니다. 문서 구조를 정확히 맞추는 것이 더 중요합니다.

---

## 흔한 오류 & 해결

🎯 **학생 행동**: 실행 중 막힌 부분을 아래 표에서 찾아, 해당 파일만 고친 뒤 다시 실행합니다.

| 오류 상황 | 확인할 것 | 해결 방향 |
|---|---|---|
| 장면 수가 0으로 나옴 | 헤딩이 `## 장면 1` 형식인가 | 헤딩을 정확히 고침 |
| 장면 수가 3으로 나옴 | 장면 4 헤딩이 빠졌는가 | 장면 4 섹션 추가 |
| 특정 장면 필드가 빠짐 | 그 장면에 7개 줄이 있는가 | 빠진 `- field:` 줄 추가 |
| FileNotFoundError가 나옴 | 작업 위치가 `picture_diary/`인가 | `cd picture_diary` 후 실행 |
| 한글이 깨짐 | 파일을 UTF-8로 읽는가 | `encoding="utf-8"` 확인 |
| 모든 장면이 같은 구도 | 장면 목적이 다른가 | 장소, 행동, 감정, 물건으로 역할 분리 |
| prompt_en이 너무 김 | 핵심 키워드만 있는가 | 한 줄 키워드형으로 줄임 |
| 렌즈 선택이 헷갈림 | 배경 중심인가 인물 중심인가 | 배경은 24/35mm, 인물·물건은 50/85mm |

자주 헷갈리는 것은 shot과 lens입니다.  
shot은 화면에 대상이 얼마나 크게 보이는지입니다.  
lens는 공간감과 배경 느낌입니다.

예를 들어 같은 CU라도 50mm와 85mm는 느낌이 다를 수 있습니다.  
85mm는 인물이나 손에 든 물건을 더 부드럽게 강조하는 데 어울립니다.  
24mm는 공간이 넓게 보이므로 장소 소개에 어울립니다.

composition은 화면 배치입니다.  
길, 복도, 창틀이 시선을 끌면 `leading line`을 고릅니다.  
정면 구도가 또렷하면 `symmetric`을 고릅니다.  
자연스럽게 한쪽에 인물을 놓고 싶으면 `rule of thirds`를 고릅니다.

---

## 📁 산출물 파일 구조

오늘 작업이 끝나면 폴더는 아래처럼 됩니다.

```
picture_diary/
├── scene_draft_seed.md
├── scene_draft.md
├── day2_self1.py
└── dev_log.md
```

각 파일의 역할은 아래와 같습니다.

| 파일 | 역할 |
|---|---|
| scene_draft_seed.md | Day 1 self2에서 만든 장면 후보 메모 |
| scene_draft.md | 오늘 만든 4장면 정식 초안 |
| day2_self1.py | 장면 수와 필드 존재 여부 확인 |
| dev_log.md | 오늘의 선택과 막힌 점 기록 |

오늘 새로 만들어야 하는 파일은 두 개입니다.

```
scene_draft.md
day2_self1.py
```

기록 파일은 이어쓰기입니다.

```
dev_log.md
```

Day 2 self2에서 새로 생길 파일은 아직 만들지 않습니다.

```
scene_prompts.json
outputs/scene01_fal.png
```

위 두 파일은 다음 세션에서 다룹니다. 오늘 미리 만들 필요가 없습니다.

---

## 🛡️ 안전 수칙

🎯 **학생 행동**: 오늘 파일에 API 키, 계정 정보, 민감한 개인 정보를 쓰지 않았는지 확인합니다.

오늘은 API를 호출하지 않습니다. 따라서 `.env`를 열 필요가 없습니다.

`scene_draft.md`에는 그림으로 표현할 수 있는 일기 장면만 씁니다.  
실명, 전화번호, 주소, 학교 세부 위치처럼 민감한 정보는 쓰지 않습니다.  
필요하면 일반 표현으로 바꿉니다. 예를 들어 구체적인 주소 대신 아래처럼 씁니다.

```
near a small convenience store
```

또는 아래처럼 씁니다.

```
on a quiet rainy street
```

`prompt_en`에는 계정명이나 실제 신상 정보를 넣지 않습니다.  
이미지 생성 모델이 장면을 이해할 정도의 정보만 남깁니다.

또한 오늘은 seed 파일을 덮어쓰지 않습니다.  
`scene_draft_seed.md`는 이전 산출물이므로 읽기용으로 둡니다.  
새로운 내용은 `scene_draft.md`에 씁니다.

파일 이름을 바꾸지 않습니다. 다음 세션 코드가 정해진 파일명을 기준으로 읽기 때문입니다.

---

## 30분 룰

🎯 **학생 행동**: 같은 오류로 30분 이상 막히면, 반복 실행을 멈추고 상황을 정리해 도움을 요청합니다.

아래 세 가지를 그대로 적습니다.

```
1. 지금 실행한 명령:
2. 터미널에 나온 메시지:
3. 내가 확인한 파일:
```

도움을 요청할 때는 파일 전체를 한꺼번에 보내기보다, 먼저 오류가 난 부분을 보여 줍니다.  
특히 아래 정보가 중요합니다.

- 현재 위치를 보여 주는 `pwd`
- 파일 목록을 보여 주는 `ls`
- 실행한 명령
- 화면에 나온 메시지
- `scene_draft.md`의 장면 헤딩 부분
- `day2_self1.py`의 함수 이름 부분

30분을 넘기면 같은 곳을 계속 고치기 쉽습니다.  
그럴 때는 장면 문장을 더 꾸미기보다 구조부터 확인합니다.

오늘 멈춤 기준은 간단합니다.  
`scene_draft.md`에 4장면이 있고, 각 장면에 7필드가 있으면 다음 세션으로 넘어갈 준비가 된 것입니다.  
남은 표현 다듬기는 Day 2 self2에서 JSON으로 옮기며 이어갑니다.
