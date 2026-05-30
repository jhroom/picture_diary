# Day 3 self2: agents/image.py로 4장 자동 생성 — 실습가이드 (60분)

Block self-B 종료 (2/2)  
산출 파일: `agents/image.py`, `day3_self2.py`, `outputs/{날짜}/scene_1~4.png`  
핵심 키워드: 모델 분기, 시드 고정, 캐릭터 일관성, 4장 일괄 생성

---

## 세션 개요

| 항목 | 내용 |
|---|---|
| 세션 ID | day3-self2 |
| 오늘 목표 | self1에서 만든 scene JSON을 이미지 생성 API 입력으로 연결해 그림일기 이미지 4장을 저장한다. |
| 만드는 파일 | `picture_diary/agents/image.py`, `picture_diary/day3_self2.py` |
| 만드는 결과 | `picture_diary/outputs/2026-05-21/scene_1.png`부터 `scene_4.png`까지 |
| 하지 않는 일 | Kling 영상 생성, 비동기 폴링, 실제 영상 합성은 하지 않는다. |
| 호출 방식 (학습 의도) | `fal_client.run()` 동기 전용. 강사 day3-s3 `subscribe()` 콜백·day3-s4 `submit()`/`status()`/`result()` 폴링은 셀프 Day 4 self1·self2에서 학습. 본 self2는 "동기 호출 4번 반복 → 결과 4장 확인" 흐름. |
| self1 연결 | `agents/scene.py`의 `extract_scenes(diary_text)`와 `outputs/scene_test.json`을 입력으로 쓴다. |
| 다음 연결 | Day 4 self2에서 오늘 만든 4장 이미지를 Kling 영상 입력 이미지로 사용한다. |
| 선택 모델 | DALL-E 3 또는 fal.ai FLUX schnell 중 하나를 고른다. |
| 비용 방향 | 연습 중에는 한 모델만 선택하고, 실패 재시도 횟수를 줄인다. |

오늘의 핵심은 장면 추출이 아니라 이미지 생성 함수의 경계를 만드는 것입니다.  
`agents/scene.py`가 텍스트를 장면 데이터로 바꾸었다면, 오늘의 `agents/image.py`는 장면 데이터를 이미지 파일로 바꿉니다.

---

## 1. self1 결과 확인 + 모델 선택 (5분)

🎯 **학생 행동**: `agents/scene.py`에서 scene JSON 추출 1회 시범 실행 + 본 세션 모델 선택

먼저 오늘의 입력 자료가 준비되어 있는지 확인합니다.  
확인할 파일은 다음 두 가지입니다.

| 확인 대상 | 확인 내용 |
|---|---|
| `picture_diary/agents/scene.py` | `extract_scenes(diary_text)` 함수가 있다. |
| `picture_diary/outputs/scene_test.json` | `scene_kr`, `prompt_en` 필드가 있는 장면이 최소 3개 있다. |

터미널 위치를 `picture_diary` 폴더로 맞춥니다.

```bash
cd picture_diary
```

scene 테스트 파일을 눈으로 확인합니다.

```bash
python -m json.tool outputs/scene_test.json
```

확인할 포인트는 세 가지입니다.

- `scenes` 목록이 보이는가?
- 각 장면에 `scene_kr`가 있는가?
- 각 장면에 `prompt_en`가 있는가?

오늘은 최종 4장을 목표로 하지만, self1 결과가 3장면이면 먼저 3장으로 흐름을 확인한 뒤 4장으로 보강해도 됩니다.

모델은 하나만 선택합니다.

| 선택지 | 비용 감각 | 품질 감각 | 속도 감각 | 추천 상황 |
|---|---|---|---|---|
| DALL-E 3 | 4장 약 $0.16 | 안정적이고 지시문 반영이 좋음 | 보통 | OpenAI SDK 흐름을 유지하고 싶을 때 |
| FLUX schnell | 4장 약 $0.012 | 빠르고 저렴하며 실험에 적합 | 빠름 | 비용을 아끼며 여러 번 조정하고 싶을 때 |

선택 메모:

| 항목 | 내가 고른 값 |
|---|---|
| 오늘 사용할 모델 | (`dalle` 또는 `flux`) |
| 고른 이유 | (비용, 품질, 속도 중 하나 이상) |

오늘은 두 모델을 모두 실행해 비교하는 시간이 아닙니다.  
한 모델로 끝까지 연결해 파일 4장이 생기는 흐름을 먼저 완성하세요.

---

## 2. 캐릭터 일관성 전략 (8분)

🎯 **학생 행동**: 본인 일기 인물·풍경에 적용할 일관성 어휘 작성

이미지 4장은 서로 다른 장면이지만 같은 그림일기처럼 보여야 합니다.  
이를 위해 모든 장면에 공통으로 붙일 문장을 `COMMON_STYLE`에 넣습니다.

Day 3 s5에서 본 핵심은 두 가지입니다.

- 같은 스타일 어휘를 모든 프롬프트에 반복한다.
- 가능한 모델에서는 seed 값을 고정해 변동을 줄인다.

아래 표를 직접 채웁니다.

| 요소 | 일관성 어휘 (모든 장면 공통) |
|---|---|
| 화풍 | (예: `"watercolor diary illustration"`) |
| 색 팔레트 | (학생이 채워요) |
| 인물/풍경 묘사 | (학생이 채워요) |
| 시간대 느낌 | (학생이 채워요) |
| 선 느낌 | (학생이 채워요) |

좋은 공통 어휘는 짧고 반복 가능해야 합니다.  
예시는 참고만 하고 본인 일기에 맞게 바꿉니다.

```
watercolor diary illustration, soft pastel palette, cozy everyday mood, consistent main character
```

풍경 중심 일기라면 인물 대신 장소의 반복성을 강조해도 됩니다.

```
watercolor diary illustration, soft rainy city palette, quiet neighborhood scenery, gentle morning light
```

공통 어휘가 너무 길면 장면별 내용이 묻힐 수 있습니다.  
한 줄 안에서 화풍, 색감, 반복 대상만 담습니다.

---

## 3. agents/image.py 함수 골격 작성 (15분)

🎯 **학생 행동**: `agents/image.py` 새 파일, 5개 함수 골격 작성

오늘 새로 만들 파일은 다음 위치입니다.

```
picture_diary/agents/image.py
```

이 파일은 이미지 생성 전용 도구 상자입니다.  
함수는 5개로 나눕니다.

| 함수 | 역할 |
|---|---|
| `call_dalle()` | DALL-E 3로 1장 생성하고 이미지 URL을 돌려준다. |
| `call_flux()` | FLUX schnell로 1장 생성하고 이미지 URL을 돌려준다. |
| `generate_image()` | 사용자가 고른 모델에 따라 위 두 함수 중 하나를 호출한다. |
| `save_image()` | URL에서 이미지를 내려받아 파일로 저장한다. |
| `batch_generate()` | scene 목록을 돌며 여러 장을 저장한다. |

아래 골격을 그대로 옮긴 뒤 빈 부분을 채웁니다.

```python
# agents/image.py — DALL-E 또는 FLUX 분기 이미지 생성
import os, requests, json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import fal_client

load_dotenv()

COMMON_STYLE = ""  # ← 캐릭터 일관성 어휘 (§2에서 정한 화풍·색·인물 표현 1줄)


def call_dalle(prompt: str, seed: int | None = None) -> str:
    """DALL-E 3로 1장 생성, URL 반환."""
    # 여기에 OpenAI() 클라이언트 + client.images.generate(...) 호출 코드를 채워요.
    # 힌트: DALL-E 3는 seed 인자를 직접 받지 않으므로 prompt에 "seed: N" 텍스트로 표현하거나 무시.
    return ""


def call_flux(prompt: str, seed: int = 42) -> str:
    """FLUX로 1장 생성, URL 반환. seed로 일관성 강화."""
    # 여기에 fal_client.run("fal-ai/flux/schnell", arguments={..., "seed": seed})를 호출하는 코드를 채워요.
    # 힌트: 응답 구조는 result["images"][0]["url"].
    return ""


def generate_image(prompt: str, model: str = "dalle", seed: int = 42) -> str:
    """모델 분기 함수. DALL-E 또는 FLUX 호출."""
    # 여기에 model 분기 (dalle/flux) 후 위 두 함수 호출 → URL 반환.
    return ""


def save_image(url: str, out_path: Path) -> None:
    # 여기에 requests.get + write_bytes 패턴 (day1_self1.py에서 가져온 재사용 코드).
    pass


def batch_generate(scenes: list[dict], model: str, out_dir: Path) -> list[Path]:
    """scenes 리스트를 받아 4장 일괄 생성 후 저장 경로 반환. try/except로 한 장 실패 시 격리."""
    # 여기에 for 루프 + try/except + generate_image + save_image 호출 패턴을 채워요.
    # 힌트: 각 scene["prompt_en"] + COMMON_STYLE 결합. seed는 scene_id로 고정.
    saved: list[Path] = []
    return saved
```

작성 순서는 아래처럼 진행합니다.

| 순서 | 할 일 |
|---|---|
| 1 | `import`와 `load_dotenv()`를 먼저 둔다. |
| 2 | `COMMON_STYLE`에 §2에서 만든 한 줄을 넣는다. |
| 3 | `call_dalle()` 또는 `call_flux()` 중 내가 선택한 모델부터 채운다. |
| 4 | `generate_image()`에서 `model` 값으로 분기한다. |
| 5 | `save_image()`에서 저장 폴더 생성을 함께 처리한다. |
| 6 | `batch_generate()`에서 한 장 실패가 전체 중단으로 번지지 않게 감싼다. |

모델 분기에서 문자열은 소문자로 맞추면 실수가 줄어듭니다.

```python
model = model.lower()
```

저장 파일명은 `scene_1.png`, `scene_2.png`처럼 단순하게 갑니다.  
프롬프트 결합은 `prompt_en` 뒤에 `COMMON_STYLE`을 붙이는 방식으로 생각합니다.  
한 장이 실패해도 다음 장면을 계속 진행하게 만드는 것이 오늘의 안정성 포인트입니다.

---

## 4. day3_self2.py 통합 실행 코드 작성 (10분)

🎯 **학생 행동**: `agents/scene.py` + `agents/image.py` 호출 + 4장 일괄 생성

오늘 두 번째 새 파일은 다음 위치입니다.

```
picture_diary/day3_self2.py
```

이 파일은 실행 버튼 역할입니다.  
`agents/image.py`가 도구 상자라면 `day3_self2.py`는 오늘의 작업 순서를 담은 실행 파일입니다.

아래 골격을 먼저 작성합니다.

```python
# day3_self2.py
from pathlib import Path
from datetime import date
import json
from agents.image import batch_generate

# 여기에 scene_prompts.json 또는 agents/scene.py 결과를 로드하고
# outputs/{오늘 날짜}/ 폴더에 4장 일괄 생성하는 코드를 채워요.
# 힌트: today = date.today().isoformat() → out_dir = Path("outputs") / today.
```

입력 방식은 둘 중 하나를 고릅니다.

| 방식 | 설명 | 추천 상황 |
|---|---|---|
| 저장 JSON 로드 | `outputs/scene_test.json`을 읽어 사용한다. | self1 결과를 이미 저장한 경우 |
| 함수 직접 호출 | `agents.scene.extract_scenes()`를 호출한다. | 일기 파일에서 바로 이어가고 싶은 경우 |

처음에는 저장 JSON 로드 방식이 더 단순합니다.  
파일 경로를 한 번만 확인하면 API 호출 비용이 드는 앞단을 반복하지 않아도 됩니다.

작업 흐름 메모:

| 순서 | 실행 파일에서 할 일 |
|---|---|
| 1 | `outputs/scene_test.json`을 연다. |
| 2 | JSON에서 장면 목록을 꺼낸다. |
| 3 | 오늘 날짜 폴더를 만든다. |
| 4 | `batch_generate(scenes[:4], model, out_dir)`를 호출한다. |
| 5 | 저장된 파일 경로를 출력해 눈으로 확인한다. |

모델 값은 처음에는 코드 안에 직접 적어도 됩니다.

```python
model = "flux"  # 또는 "dalle"
```

수업 중에는 환경변수나 CLI 인자까지 확장하지 않아도 됩니다.  
오늘의 목표는 구조를 단순하게 완성하는 것입니다.

---

## 5. 실행하고 4장 비교 (8분)

🎯 **학생 행동**: `python day3_self2.py` → 4장 확인 + 캐릭터 일관성 자체 평가

실행 전 마지막으로 `.env`를 확인합니다.

| 모델 | 필요한 키 |
|---|---|
| DALL-E 3 | `OPENAI_API_KEY` |
| FLUX schnell | fal.ai 인증 설정 또는 `FAL_KEY` |

실행합니다.

```bash
python day3_self2.py
```

저장 폴더를 확인합니다.

```bash
ls -lh outputs/2026-05-21
```

다음 파일명이 보이면 흐름이 이어진 것입니다.

```
scene_1.png
scene_2.png
scene_3.png
scene_4.png
```

4장을 열어 보고 아래 표를 직접 채웁니다.

| 장면 | 분위기 일관 | 색감 일관 | 인물/풍경 일관 |
|---|---|---|---|
| scene_1 | (✅/❌) | (✅/❌) | (✅/❌) |
| scene_2 | (✅/❌) | (✅/❌) | (✅/❌) |
| scene_3 | (✅/❌) | (✅/❌) | (✅/❌) |
| scene_4 | (✅/❌) | (✅/❌) | (✅/❌) |

비교할 때는 "예쁘다", "별로다"보다 일관성을 먼저 봅니다.  
문제가 있으면 API를 바로 다시 여러 번 호출하지 말고 `COMMON_STYLE` 한 줄부터 고칩니다.

---

## 6. dev_log.md 이어쓰기 + Day 4 입력 자료 검증 (3분)

🎯 **학생 행동**: `outputs/{날짜}/scene_1~4.png`가 Day 4 self2 Kling 영상 입력으로 적합한지 확인

오늘 결과는 Day 4에서 영상 입력 이미지로 쓰입니다.  
따라서 이미지가 존재하는지만 보지 말고 개수, 파일 크기, 해상도를 확인합니다.

파일 개수 확인:

```bash
ls outputs/2026-05-21/scene_*.png | wc -l
```

파일 크기 확인:

```bash
ls -lh outputs/2026-05-21/scene_*.png
```

해상도 확인은 macOS에서 다음 명령을 사용할 수 있습니다.

```bash
sips -g pixelWidth -g pixelHeight outputs/2026-05-21/scene_1.png
```

4장 모두 같은 방식으로 확인합니다.

`dev_log.md`에는 아래 형식으로 이어 씁니다.

```markdown
## Day 3 self2

- 사용 모델: (dalle 또는 flux)
- COMMON_STYLE: (내가 사용한 공통 스타일 한 줄)
- 생성 결과: outputs/2026-05-21/scene_1~4.png
- 재시도한 장면: (있으면 기록)
- Day 4 입력 가능 여부: (가능 / 보류)
```

로그에는 API 키, 계정 정보, 결제 정보, 원본 비밀 문자열을 적지 않습니다.  
Day 4에서 다시 확인할 수 있도록 파일 경로와 모델 선택만 남기면 충분합니다.

---

## 7. 자기 점검 (10분)

아래 항목을 스스로 확인합니다.

- [ ] `picture_diary/agents/image.py`를 새로 만들었다.
- [ ] `call_dalle()`, `call_flux()`, `generate_image()`, `save_image()`, `batch_generate()` 골격이 있다.
- [ ] `COMMON_STYLE`에 네 장 공통 스타일 문장을 넣었다.
- [ ] `generate_image()`에서 `dalle`과 `flux` 모델 분기를 처리했다.
- [ ] `day3_self2.py`에서 scene JSON을 읽거나 scene 추출 함수를 호출한다.
- [ ] `outputs/{날짜}` 폴더에 이미지 파일이 저장된다.
- [ ] `scene_1.png`부터 `scene_4.png`까지 총 4장을 확인했다.
- [ ] `dev_log.md`에 모델, 스타일, 결과 폴더를 기록했다.

**Day 4 self1 미리보기:**  
다음 self1에서는 비동기 폴링 패러다임을 배워요.  
Kling API에 영상 `submit` 후 `job_id`로 상태를 폴링하는 패턴입니다.  
오늘은 동기식 이미지 생성 흐름을 끝내고, 다음에는 오래 걸리는 영상 작업을 기다리는 구조로 넘어갑니다.

---

## 흔한 오류 & 해결

| 오류 | 증상 | 해결 |
|---|---|---|
| 모델 분기 if 누락 | `model="flux"`로 바꿔도 항상 같은 API만 호출된다. | `generate_image()`에서 `if`, `elif`, `else` 흐름을 분명히 나눈다. |
| 응답 구조 혼동 | URL을 꺼내는 줄에서 속성 오류 또는 키 오류가 난다. | DALL-E와 FLUX의 URL 위치가 다르다는 점을 함수별로 분리해 확인한다. |
| 시드 미고정 | 네 장의 인물, 풍경, 색감이 크게 흔들린다. | FLUX 사용 시 `seed`를 장면별로 일관된 규칙에 따라 넣는다. |
| 폴더 생성 누락 | 파일 저장 단계에서 `FileNotFoundError`가 난다. | 저장 전에 `out_path.parent.mkdir(parents=True, exist_ok=True)` 흐름을 넣는다. |
| `prompt_en` 필드 누락 | 특정 장면에서 프롬프트 문자열을 읽지 못한다. | self1 결과 JSON의 필드 이름을 먼저 확인한다. |
| API 키 위치 오류 | 인증 관련 오류가 난다. | `.env` 위치와 키 이름을 다시 확인한다. |

---

## 📁 산출물 파일 구조

오늘 종료 시 목표 구조는 아래와 같습니다.

```
picture_diary/
├── agents/
│   ├── __init__.py
│   ├── scene.py
│   └── image.py
├── diary.md
├── day3_self2.py
├── dev_log.md
├── outputs/
│   ├── scene_test.json
│   └── 2026-05-21/
│       ├── scene_1.png
│       ├── scene_2.png
│       ├── scene_3.png
│       └── scene_4.png
└── .env
```

날짜 폴더명은 실행 날짜에 따라 달라질 수 있습니다.  
강의 흐름에서는 `2026-05-21`을 기준 예시로 사용합니다.

---

## 🛡️ 안전 수칙 + 비용 가드

- API 키는 반드시 `.env`에 둡니다.
- 코드 파일, 마크다운 파일, 질문 메시지에 키 원문을 붙이지 않습니다.
- `.gitignore`에 `.env`가 포함되어 있는지 확인합니다.
- 오늘은 비용이 발생할 수 있으므로 한 모델만 선택합니다.

비용 기준:

| 모델 | 4장 비용 감각 |
|---|---|
| DALL-E 3 | 약 $0.16 |
| FLUX schnell | 약 $0.012 |

누적 비용은 `dev_log.md`에 "모델, 장수, 재시도 횟수"만 짧게 기록합니다.  
이미지 품질이 마음에 들지 않아도 즉시 여러 번 재생성하지 않습니다.  
먼저 `COMMON_STYLE`을 고치고, 장면별 `prompt_en`이 충분히 구체적인지 확인합니다.  
재시도는 가장 문제가 큰 한 장부터 합니다.

---

## 30분 룰

30분 이상 막히면 아래 P3 프롬프트 카드를 강사에게 보여 주세요.

```
[P3 도움 요청 카드]

1. 지금 단계:
   - agents/image.py 작성 중 / day3_self2.py 작성 중 / 실행 중 / 저장 확인 중

2. 선택 모델:
   - dalle / flux

3. 마지막으로 실행한 명령:
   - 예: python day3_self2.py

4. 오류 메시지:
   - 터미널의 마지막 5~10줄을 붙여요.

5. 확인한 파일:
   - outputs/scene_test.json 있음 / 없음
   - outputs/2026-05-21 폴더 있음 / 없음

6. 내가 예상한 흐름:
   - scene JSON 읽기 → 이미지 URL 받기 → PNG 저장
```

도움을 요청할 때 API 키는 절대 포함하지 않습니다.

오늘의 멈춤 기준은 명확합니다.  
`outputs/{날짜}/scene_1~4.png`가 준비되고, Day 4 입력으로 사용할 수 있음을 확인하면 self-B가 종료됩니다.