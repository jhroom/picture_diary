# Day 2 self2: 4장면 프롬프트 JSON + fal.ai 첫 호출 — 실습가이드 (60분)

Block self-B 종료 (2/2) — 본 세션 50분 안에 압축  
산출 파일: `scene_prompts.json`, `day2_self2.py`, `outputs/scene01_fal.png`, `dev_log.md`(이어쓰기), `.env`(FAL_KEY 추가)  
핵심 키워드: JSON 스키마, fal-client, subscribe(), FLUX-schnell, 비용 가드

---

## 세션 개요

| 항목 | 내용 |
|---|---|
| 세션 ID | day2-self2 |
| 시간 | 17:00~17:50 본 활동 + 17:50~18:00 자기 점검 |
| 형식 | 자기주도 셀프 스터디 |
| 이전 연결 | self1의 `scene_draft.md` (4장면 초안) |
| 다음 연결 | Day 3 self1 — `agents/scene.py`로 일기→scenes JSON 자동 추출 |

오늘은 self1에서 만든 4장면 초안을 `scene_prompts.json`으로 정리하고, fal.ai의 FLUX-schnell 모델로 첫 장면 1장만 생성합니다.

핵심은 두 가지입니다.

1. 장면 정보를 4장면 × 7필드 JSON으로 저장하기
2. DALL-E와 다른 fal.ai 응답 구조를 확인하기

오늘은 4장을 한꺼번에 만들지 않습니다.  
처음 호출은 반드시 1장만 합니다.  
비용을 작게 유지하고, 응답 구조를 먼저 확인하기 위해서입니다.

---

## 📁 산출물 파일 구조

오늘 작업이 끝나면 `picture_diary/` 안이 아래처럼 됩니다.

```
picture_diary/
├── .env
├── diary.md
├── scene_draft.md
├── scene_prompts.json
├── day2_self2.py
├── dev_log.md
└── outputs/
    └── scene01_fal.png
```

각 파일의 역할은 다음과 같습니다.

| 파일 | 역할 |
|---|---|
| `.env` | `OPENAI_API_KEY`, `FAL_KEY`를 저장합니다. |
| `scene_draft.md` | self1에서 만든 4장면 초안입니다. |
| `scene_prompts.json` | 오늘 새로 만드는 4장면 프롬프트 JSON입니다. |
| `day2_self2.py` | fal.ai FLUX-schnell을 1회 호출하는 연습 파일입니다. |
| `outputs/scene01_fal.png` | FLUX-schnell로 만든 첫 장면 이미지입니다. |
| `dev_log.md` | 오늘 막힌 부분과 비교 관찰을 기록합니다. |

작업 위치는 `picture_diary/` 폴더입니다. 터미널에서 먼저 위치를 확인하세요.

```bash
pwd
ls
```

`scene_draft.md`가 보이면 오늘 작업을 시작할 수 있습니다.

---

## 🛡️ 안전 수칙 + 비용 가드

API 키는 비밀번호처럼 다룹니다. `FAL_KEY`도 `OPENAI_API_KEY`와 같은 보안 규칙을 적용합니다.

- 키는 `.env`에만 적습니다.
- 코드 파일에 키를 직접 적지 않습니다.
- 브라우저 AI 도우미나 채팅창에 키를 붙여넣지 않습니다.
- 화면 공유 중에는 `.env` 파일을 열어 두지 않습니다.
- 제출 파일에는 키가 포함되지 않게 확인합니다.

비용 가드는 오늘 특히 중요합니다.

| 항목 | 오늘 기준 |
|---|---|
| 생성 모델 | FLUX-schnell |
| 생성 수량 | 첫 장면 1장 |
| 예상 비용 | 약 $0.003 |
| 무료 크레딧 기준 | fal.ai 무료 크레딧 $1 안에서 충분 |
| 금지 행동 | 처음부터 4장 이상 반복 생성 |

오늘은 `num_images`를 1로 둡니다.  
이미지 결과가 마음에 들지 않아도 바로 여러 번 반복하지 않습니다.  
먼저 `prompt_en`, 응답 구조, 저장 경로가 맞는지 확인합니다.

---

## 30분 룰

같은 문제로 30분 이상 막히면 혼자 계속 반복하지 않습니다.  
아래 세 가지를 정리해서 강사에게 보여 주세요.

```
1. 지금 실행한 명령:
2. 터미널 오류 메시지:
3. 내가 확인한 파일:
```

오류 메시지는 일부만 요약하지 말고 그대로 보여 주는 편이 좋습니다.  
특히 오늘은 다음 오류가 자주 나옵니다.

- `.env` 파일 위치 오류
- `FAL_KEY` 이름 오타
- `fal_client` 패키지 미설치
- JSON 마지막 콤마 오류
- DALL-E 응답 구조와 fal.ai 응답 구조 혼동

---

## 1. self1 결과 확인 + FAL_KEY 발급 (8분)

🎯 **학생 행동**: `scene_draft.md` 4장면을 다시 읽고, fal.ai 계정을 만든 뒤 `FAL_KEY`를 `.env`에 추가합니다.

먼저 self1 결과를 엽니다.

```bash
ls
cat scene_draft.md
```

확인할 것은 네 가지입니다.

- 장면이 4개인지
- 각 장면이 그림으로 보이는지
- 샷, 앵글, 조명, 구도 어휘가 있는지
- 민감 정보나 API 키가 들어 있지 않은지

다음으로 fal.ai 키를 발급합니다.

1. 브라우저에서 fal.ai에 접속합니다.
2. 계정을 만들거나 로그인합니다.
3. Settings 메뉴로 이동합니다.
4. API Keys 메뉴를 엽니다.
5. 새 키를 생성합니다.
6. 키를 복사해 `.env`에 넣습니다.

`.env`는 아래 형식을 사용합니다.

```
OPENAI_API_KEY=# 여기에 OpenAI API 키를 채워요
FAL_KEY=# 여기에 fal.ai API 키를 채워요
```

주의할 점은 `FAL_KEY`라는 이름입니다.  
`FAL_API_KEY`, `fal_key`, `FAL TOKEN`처럼 다른 이름으로 쓰면 코드에서 찾지 못합니다.

패키지도 설치합니다.

```bash
uv pip install fal-client
```

`requests`와 `python-dotenv`가 이미 설치되어 있지 않다면 함께 설치합니다.

```bash
uv pip install requests python-dotenv
```

설치 후에는 아래 명령으로 패키지 이름을 확인합니다.

```bash
uv pip show fal-client
```

보안 확인도 합니다.

```bash
grep -n "FAL_KEY" .env
```

이 명령은 키가 `.env`에 있는지만 확인하기 위한 것입니다.  
터미널 출력에 키 전체가 보이면 다른 사람에게 화면을 공유하지 않습니다.

---

## 2. JSON 스키마 설계 (8분)

🎯 **학생 행동**: `scene_prompts.json`의 구조를 머릿속으로 먼저 설계합니다.

오늘 JSON은 장면 객체 4개를 가진 배열입니다. 각 장면은 7개 필드를 가집니다.

```json
{
  "scenes": [
    {
      "scene_id": 1,
      "scene_kr": "# 여기에 self1 scene_draft.md 1장면 한 줄 설명을 채워요",
      "shot": "# 여기에 WS|MS|BS|CU|ECU 중 하나를 채워요",
      "angle": "# 여기에 eye-level|low|high 중 하나를 채워요",
      "lighting": "# 여기에 soft|rim|backlit 중 하나를 채워요",
      "lens": "# 여기에 24mm|35mm|50mm|85mm 중 하나를 채워요",
      "prompt_en": "# 여기에 위 어휘를 결합한 영문 1줄을 채워요"
    }
  ]
}
```

필드 역할은 아래와 같습니다.

| 필드 | 역할 |
|---|---|
| `scene_id` | 장면 번호입니다. 1부터 4까지 씁니다. |
| `scene_kr` | self1 장면 설명을 한국어 한 줄로 옮깁니다. |
| `shot` | 화면 거리입니다. WS, MS, BS, CU, ECU 중 하나를 씁니다. |
| `angle` | 카메라 시점입니다. eye-level, low, high 중 하나를 씁니다. |
| `lighting` | 빛의 느낌입니다. soft, rim, backlit 중 하나를 씁니다. |
| `lens` | 렌즈 느낌입니다. 24mm, 35mm, 50mm, 85mm 중 하나를 씁니다. |
| `prompt_en` | 장면을 영어 프롬프트 한 줄로 정리합니다. |

self1의 `scene_draft.md`와 달라진 점도 확인합니다.

| self1 초안 | 오늘 JSON |
|---|---|
| `light` | `lighting`으로 이름을 바꿉니다. |
| `composition` | 오늘 JSON에는 넣지 않습니다. |
| 없음 | `lens`를 새로 추가합니다. |

`composition`을 버리는 이유는 오늘 목표가 이미지 API 첫 호출이기 때문입니다.  
필드를 조금 줄이고, 모델 호출에 바로 쓰기 쉬운 항목을 우선합니다.  
`lens`는 화면 느낌을 안정시키기 위한 새 필드입니다.

대략적인 선택 기준은 다음과 같습니다.

| 렌즈 | 느낌 |
|---|---|
| 24mm | 넓은 공간, 배경이 중요한 장면 |
| 35mm | 거리감 있는 일상 장면 |
| 50mm | 자연스러운 인물 장면 |
| 85mm | 얼굴, 표정, 배경 흐림 |

---

## 3. scene_prompts.json 작성 (10분)

🎯 **학생 행동**: `scene_draft.md` 4장면을 오늘 스키마로 변환해 `scene_prompts.json`으로 저장합니다.

파일 이름은 정확히 `scene_prompts.json`입니다.  
`scene_prompt.json`, `scene_prompts.md`처럼 다르게 만들면 다음 세션에서 연결되지 않습니다.

작성 순서는 다음을 권장합니다.

1. `scene_id` 1~4를 먼저 적습니다.
2. `scene_kr`에 self1 장면 한 줄 설명을 옮깁니다.
3. `shot`, `angle`, `lighting`을 선택합니다.
4. `lens`를 선택합니다.
5. 마지막에 `prompt_en`을 한 줄로 씁니다.

JSON은 문법이 엄격합니다.  
문자열은 큰따옴표로 감싸야 합니다.  
마지막 항목 뒤에는 콤마를 붙이지 않습니다.

아래 검증 스크립트를 그대로 실행합니다.

```python
# 검증: scene_prompts.json 파싱 + 4장면 × 7필드 확인
import json
from pathlib import Path

REQUIRED_FIELDS = ["scene_id", "scene_kr", "shot", "angle", "lighting", "lens", "prompt_en"]

data = json.loads(Path("scene_prompts.json").read_text(encoding="utf-8"))
scenes = data.get("scenes", [])
print(f"장면 수: {len(scenes)}")

for i, scene in enumerate(scenes, 1):
    missing = [f for f in REQUIRED_FIELDS if f not in scene]
    if missing:
        print(f"장면 {i} 누락 필드: {missing}")
    else:
        print(f"장면 {i} OK — shot={scene['shot']}, angle={scene['angle']}")
```

예상 출력은 아래와 비슷합니다.

```
장면 수: 4
장면 1 OK — shot=BS, angle=eye-level
장면 2 OK — shot=CU, angle=low
장면 3 OK — shot=MS, angle=eye-level
장면 4 OK — shot=WS, angle=high
```

출력이 다르게 나와도 괜찮습니다.  
중요한 것은 장면 수가 4이고, 각 장면에 7개 필드가 모두 있는 것입니다.

`prompt_en`은 길게 쓰지 않아도 됩니다.  
장면, 샷, 앵글, 조명, 렌즈가 한 줄에 들어가면 충분합니다.

```
장면 내용 + shot + angle + lighting + lens + mood
```

---

## 4. day2_self2.py 함수 골격 작성 (15분)

🎯 **학생 행동**: `day2_self2.py`를 새로 만들고 아래 함수 골격의 빈 부분을 채웁니다.

오늘 파일은 4개 함수로 나눕니다.

| 함수 | 역할 |
|---|---|
| `load_keys()` | `.env`에서 키를 읽고 마스킹 출력합니다. |
| `load_first_prompt()` | `scene_prompts.json`의 첫 번째 `prompt_en`을 읽습니다. |
| `call_flux_schnell()` | FLUX-schnell을 1장만 호출하고 URL을 받습니다. |
| `save_image()` | URL의 이미지 바이트를 내려받아 저장합니다. |

아래 코드를 `day2_self2.py`에 붙여 넣고, 주석이 있는 부분만 채웁니다.  
완성 전에는 실행해도 이미지가 생성되지 않을 수 있습니다.

```python
# day2_self2.py — fal.ai FLUX-schnell 첫 호출 (1장 시범)
import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import fal_client


def load_keys() -> None:
    """.env에서 FAL_KEY와 OPENAI_API_KEY를 로드합니다."""
    # 여기에 load_dotenv() 호출 + os.getenv("FAL_KEY") 가져오기 + 첫 5자 마스킹 출력을 채워요.
    # 힌트: FAL_KEY가 없으면 fal-client가 작동하지 않아요.
    # 힌트: print(f"FAL_KEY: {key[:5]}...") 형태로 마스킹 출력해요.
    pass


def load_first_prompt() -> str:
    """scene_prompts.json에서 첫 번째 장면의 prompt_en을 반환합니다."""
    # 여기에 scene_prompts.json을 json.load로 읽고 scenes[0]["prompt_en"]을 반환하는 코드를 채워요.
    # 힌트: Path("scene_prompts.json").read_text(encoding="utf-8")로 파일을 읽어요.
    return ""


def call_flux_schnell(prompt: str) -> str:
    """FLUX-schnell로 이미지 1장 생성, URL을 반환합니다."""
    # 여기에 fal_client.subscribe("fal-ai/flux/schnell", arguments={"prompt": prompt, "num_images": 1})를 호출하고
    #   result["images"][0]["url"]을 반환하는 코드를 채워요.
    # 힌트: 응답 구조는 DALL-E와 다릅니다.
    #   OpenAI = response.data[0].url
    #   fal.ai = result["images"][0]["url"]
    return ""


def save_image(url: str, out_path: Path) -> None:
    """URL의 PNG 바이트를 내려받아 out_path에 저장합니다."""
    # 여기에 requests.get(url) + out_path.write_bytes(response.content) 코드를 채워요.
    # 힌트: day1_self1.py에서 작성한 패턴을 재사용해요.
    pass


if __name__ == "__main__":
    load_keys()
    prompt = load_first_prompt()
    print(f"[프롬프트] {prompt[:60]}...")
    url = call_flux_schnell(prompt)
    print(f"[FLUX URL] {url[:60]}...")
    out_path = Path("outputs") / "scene01_fal.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(url, out_path)
    print(f"[저장 완료] {out_path}")
```

함수별 힌트는 아래처럼 읽으면 됩니다.

- `load_keys()`는 `.env`를 읽는 함수입니다. 키 전체를 출력하지 말고 앞 5자만 보이게 합니다.
- `load_first_prompt()`는 첫 번째 장면만 가져옵니다. 오늘은 비용 가드를 위해 4장면 전체를 호출하지 않습니다.
- `call_flux_schnell()`은 fal.ai 호출을 담당합니다. 모델 이름은 `"fal-ai/flux/schnell"`이고 `num_images`는 반드시 1로 시작합니다.
- `save_image()`는 이미지 URL을 파일로 저장합니다. `outputs` 폴더는 마지막 실행 블록에서 만들어집니다.

---

## 5. 실행하고 결과 확인 + DALL-E 비교 (8분)

🎯 **학생 행동**: `python day2_self2.py`를 실행하고 `outputs/scene01_fal.png`가 생성되었는지 확인합니다.

실행합니다.

```bash
python day2_self2.py
```

예상 출력은 아래와 비슷합니다.

```
FAL_KEY: sk-fa...
[프롬프트] morning sunlight cafe, young woman reading book, CU sh...
[FLUX URL] https://fal.run/files/...
[저장 완료] outputs/scene01_fal.png
```

파일이 생겼는지 확인합니다.

```bash
ls outputs
```

Day 1에서 만든 `outputs/scene01_dalle.png`가 있다면 같이 열어 봅니다.  
두 이미지를 보고 아래 표를 채웁니다.

| 모델 | 분위기 | 디테일 | 응답 구조 |
|---|---|---|---|
| DALL-E 3 | (학생이 채워요) | (학생이 채워요) | `response.data[0].url` |
| FLUX-schnell | (학생이 채워요) | (학생이 채워요) | `result["images"][0]["url"]` |

가장 중요한 차이는 응답 구조입니다.  
DALL-E에서 쓰던 `response.data[0].url`을 fal.ai에 그대로 쓰면 안 됩니다.  
fal.ai 결과는 딕셔너리 구조로 보고, `result["images"][0]["url"]`에서 URL을 꺼냅니다.

이 차이를 `dev_log.md`에 한 줄로 남깁니다.

비용도 기록합니다.  
오늘 FLUX-schnell 1장은 약 $0.003 수준입니다.  
Day 2 누적 비용은 DALL-E 약 $0.16과 FLUX 약 $0.003을 합쳐 $0.20 안쪽으로 관리합니다.

---

## 6. dev_log.md 이어쓰기 + Day 3 입력 자료 검증 (3분)

🎯 **학생 행동**: `dev_log.md`에 오늘 작업을 이어 쓰고, `scene_prompts.json`이 Day 3 self1 입력으로 쓸 수 있는지 확인합니다.

Day 3 self1에서 `agents/scene.py`를 작성하면, 이 `scene_prompts.json` 스키마를 입력으로 사용합니다.  
7개 필드가 정확히 채워져 있어야 자동화 연결이 됩니다.

아래 스크립트를 실행해 Day 3 연결 준비를 확인합니다.

```python
# Day 3 입력 자료 체크 스크립트
import json
from pathlib import Path

data = json.loads(Path("scene_prompts.json").read_text(encoding="utf-8"))
scenes = data.get("scenes", [])

required = ["scene_id", "scene_kr", "shot", "angle", "lighting", "lens", "prompt_en"]
all_ok = True

for scene in scenes:
    missing = [f for f in required if not scene.get(f)]
    if missing:
        print(f"scene {scene.get('scene_id', '?')} 미완성 필드: {missing}")
        all_ok = False

if all_ok and len(scenes) == 4:
    print("✅ Day 3 self1 연결 준비 완료 — 4장면 × 7필드 모두 채워짐")
else:
    print("⚠️ 미완성 항목이 있어요. 위 결과를 확인해 채워요.")
```

`dev_log.md`에는 아래 형식으로 이어 씁니다.

```markdown
## Day 2 self2 — scene_prompts.json + fal.ai 첫 호출

- 완료 시각: 17:50
- 생성 파일: scene_prompts.json, day2_self2.py, outputs/scene01_fal.png
- FLUX vs DALL-E 차이: (학생이 채워요)
- 막힌 부분: (있으면 채워요)
```

막힌 부분이 없으면 "없음"이라고 적어도 됩니다.  
중요한 것은 오늘의 입력 구조와 API 응답 차이를 기록하는 것입니다.

---

## 7. 자기 점검 (10분)

아래 체크리스트를 하나씩 확인합니다.

- [ ] `scene_prompts.json` 파일이 있어요.
- [ ] 4장면이 모두 있어요.
- [ ] 각 장면에 7개 필드(`scene_id`, `scene_kr`, `shot`, `angle`, `lighting`, `lens`, `prompt_en`)가 채워져 있어요.
- [ ] `outputs/scene01_fal.png` 파일이 생성되었어요.
- [ ] `.env`에 `FAL_KEY`가 있고 코드에는 키가 없어요.
- [ ] DALL-E 응답 구조(`response.data[0].url`)와 FLUX 응답 구조(`result["images"][0]["url"]`)의 차이를 이해했어요.
- [ ] `day2_self2.py` 4개 함수(`load_keys`, `load_first_prompt`, `call_flux_schnell`, `save_image`)가 모두 완성되었어요.
- [ ] `dev_log.md`에 오늘 기록을 이어썼어요.
- [ ] Day 2 누적 비용이 $0.20 이내예요 (~$0.16 DALL-E + ~$0.003 FLUX).
- [ ] `scene_prompts.json`이 Day 3 self1 `agents/scene.py` 입력 준비가 되어 있어요.

다음 셀프 세션에서는 `agents/scene.py`를 작성합니다.  
Chat JSON 모드를 이용해 일기 텍스트에서 장면 정보를 자동으로 추출하고,  
오늘 만든 `scene_prompts.json` 스키마 형식으로 저장하게 됩니다.

자기 점검이 끝나면 파일 4개를 다시 확인합니다.

```bash
ls scene_prompts.json day2_self2.py dev_log.md outputs/scene01_fal.png
```

---

## 흔한 오류 & 해결

| 오류 | 원인 | 해결 |
|---|---|---|
| `ModuleNotFoundError: fal_client` | `fal-client` 패키지 미설치 | `uv pip install fal-client` |
| `FAL_KEY`가 `None`입니다 | `.env`에 `FAL_KEY` 미입력 또는 파일 위치 오류 | 프로젝트 루트 `.env` 확인 + `FAL_KEY=...` 형식 확인 |
| `KeyError: 'images'` | FLUX 응답 구조를 DALL-E 방식으로 접근 | `result["images"][0]["url"]` 사용 (`response.data` 금지) |
| JSON 파싱 오류 | 마지막 콤마, 따옴표 누락 등 JSON 문법 오류 | JSON 검증 사이트 또는 `json.loads()` 오류 메시지 확인 |
| `outputs/scene01_fal.png`가 없음 | URL 저장 함수가 비어 있거나 경로가 다름 | `save_image()`와 `out_path` 값을 다시 확인 |
| 프롬프트가 비어 있음 | `load_first_prompt()`가 빈 문자열을 반환 | `scene_prompts.json`의 첫 장면 `prompt_en` 확인 |

오류를 고친 뒤에는 처음부터 다시 실행하지 말고, 바꾼 부분과 연결된 파일부터 확인합니다.

- JSON 오류를 고쳤다면 먼저 JSON 검증 스크립트를 실행합니다.
- 키 오류를 고쳤다면 `load_keys()` 출력만 먼저 확인합니다.
- 이미지 저장 오류를 고쳤다면 `outputs/` 폴더와 파일명을 먼저 확인합니다.

---

## 제출 전 마지막 확인

아래 5개를 마지막으로 확인합니다.

| 확인 | 기준 |
|---|---|
| 파일명 | `scene_prompts.json`, `day2_self2.py`, `outputs/scene01_fal.png` |
| 장면 수 | `scenes` 배열 안에 4개 |
| 필드 수 | 장면마다 7개 |
| 키 보안 | `.env`에만 키가 있고 코드에는 없음 |
| 다음 연결 | Day 3 self1의 `agents/scene.py` 입력으로 사용 가능 |

오늘 세션은 결과 이미지의 완성도보다 연결 구조가 더 중요합니다.  
이미지가 조금 어색해도 `scene_prompts.json`과 API 호출 흐름이 맞으면 다음 단계로 갈 수 있습니다.