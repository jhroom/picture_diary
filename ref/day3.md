# Day 3 self1: agents/scene.py로 일기→scenes JSON 자동 추출 — 실습가이드 (60분)

Block self-A 시작 (1/2)  
산출 파일: `agents/__init__.py`, `agents/scene.py`, `day3_self1.py`, `dev_log.md`(이어쓰기)  
핵심 키워드: Chat JSON 모드, JSON 스키마, 자동 추출, 일기→scenes

---

## 세션 개요

| 항목 | 내용 |
|---|---|
| 세션 ID | day3-self1 |
| 시간 | 16:00~16:50 실습 50분 + 자기 점검 10분 |
| 오늘 목표 | `diary.md`를 읽어 4장면 JSON을 자동 추출하는 `agents/scene.py`를 만든다. |
| 오늘 만드는 파일 | `agents/__init__.py`, `agents/scene.py`, `day3_self1.py`, `scene_extracted.json` |
| 이어쓰기 파일 | `dev_log.md` |
| 이전 연결 | Day 2 self2 산출물 `picture_diary/scene_prompts.json`의 4장면 × 7필드 패턴을 참고한다. |
| 다음 연결 | Day 3 self2에서 `agents/image.py`가 `scene_extracted.json`을 읽어 이미지 4장을 자동 생성한다. |
| 사용하는 도구 | OpenAI `chat.completions` + `response_format={"type": "json_object"}` |
| 오늘 하지 않는 일 | 이미지 생성, 영상 생성, 프롬프트 미감 평가, API 키 공유 |

오늘의 핵심은 사람이 직접 쓰던 장면 프롬프트 표를 코드로 자동화하는 것입니다.  
Day 2 self2에서는 `scene_prompts.json`을 직접 만들었습니다.  
오늘은 같은 일을 `agents/scene.py`가 대신 하도록 만듭니다.

- 입력은 `diary.md`입니다.
- 출력은 `scene_extracted.json`입니다.
- 출력 JSON은 Day 3 self2의 이미지 생성 입력이 됩니다.

---

## 1. scene_prompts.json 확인 + Chat JSON 모드 비유 (5분)

🎯 **학생 행동**: `scene_prompts.json`을 다시 보면서 "사람이 직접 작성한 패턴"을 모델이 자동화하는 그림을 머릿속으로 그립니다.

먼저 작업 폴더를 확인합니다.

```bash
cd picture_diary
```

Day 2 self2 결과 파일을 엽니다.

```bash
python -m json.tool scene_prompts.json
```

파일이 없다면 Day 2 self2에서 만든 위치를 다시 확인합니다.  
오늘 수업에서는 이 파일을 새로 만드는 것이 아니라, 이 파일의 구조를 참고합니다.

확인할 포인트는 네 가지입니다.

- 장면이 4개인가?
- 장면마다 반복되는 필드가 있는가?
- `scene_kr`처럼 한국어 설명이 있는가?
- `prompt_en`처럼 이미지 생성용 영어 프롬프트가 있는가?

Chat JSON 모드는 이렇게 생각하면 쉽습니다.

> **체크리스트 기반 인터뷰 양식** — 모델이 정해진 칸에 장면을 채워줘요.

일반 채팅은 자유롭게 말하는 대화입니다.  
JSON 모드는 칸이 정해진 신청서에 답을 쓰게 하는 방식입니다.

오늘은 모델에게 "좋은 답변을 해줘"라고만 말하지 않습니다.  
"반드시 `scenes`라는 JSON 키 아래에 4개 장면을 넣어줘"라고 말합니다.

사람 작업과 GPT 자동화를 비교해 봅니다.

| 항목 | 사람이 직접 작성 | GPT 자동화 |
|---|---|---|
| 장면 수 | 일기를 읽고 4개 장면을 직접 고른다. | 일기에서 4개 장면을 자동으로 고르게 한다. |
| 필드 추출 | `scene_id`, `scene_kr`, `prompt_en`을 직접 쓴다. | 정해진 JSON 스키마에 맞춰 채우게 한다. |
| 영문 번역 | 한국어 장면을 영어 프롬프트로 직접 바꾼다. | `prompt_en`을 영어로 만들게 한다. |
| 어휘 선택 | `shot`, `angle`, `lighting`을 직접 기억해 넣는다. | 시스템 프롬프트에 필수 어휘 조건을 넣는다. |
| 실수 가능성 | 필드명을 빼먹거나 장면 수가 흔들릴 수 있다. | 검증 함수로 장면 수와 필드를 확인한다. |

비교 메모:

| 질문 | 내 답 |
|---|---|
| Day 2 self2에서 가장 오래 걸린 작업은? | (학생이 채워요) |
| GPT가 자동화하면 편해질 부분은? | (학생이 채워요) |
| 자동화해도 사람이 확인해야 할 부분은? | (학생이 채워요) |

오늘 만들 흐름은 다음과 같습니다.

```
diary.md
  → agents/scene.py
  → scene_extracted.json
  → Day 3 self2 agents/image.py
  → 이미지 4장
```

이제 JSON 스키마와 시스템 프롬프트를 먼저 설계합니다.

---

## 2. JSON 스키마 + 시스템 프롬프트 설계 (10분)

🎯 **학생 행동**: `agents/scene.py`에 사용할 JSON 스키마와 시스템 프롬프트를 작성합니다.

JSON 스키마는 모델이 채워야 하는 답안지입니다.  
오늘 필요한 최소 필드는 3개입니다.

| 필드 | 뜻 | 예시 방향 |
|---|---|---|
| `scene_id` | 장면 번호 | 1, 2, 3, 4 |
| `scene_kr` | 한국어 1줄 장면 설명 | "비 오는 아침 버스를 기다리는 장면" |
| `prompt_en` | 영어 이미지 프롬프트 1줄 | shot, angle, lighting, style 포함 |

Day 2 self2의 `scene_prompts.json`에는 더 많은 필드가 있었을 수 있습니다.  
오늘은 Day 3 self2 연결에 필요한 최소 필드부터 안정적으로 만듭니다.  
필드가 적으면 검증이 쉬워집니다.  
필드가 안정되면 나중에 `style`, `negative_prompt`, `seed` 같은 필드를 확장할 수 있습니다.

아래 시스템 프롬프트 골격을 `agents/scene.py`에 넣을 예정입니다.  
빈칸은 본인 일기의 분위기에 맞게 채웁니다.

```python
SYSTEM_PROMPT = """
당신은 일기 텍스트를 분석하여 그림 4장면을 추출하는 어시스턴트입니다.
출력은 반드시 JSON 객체여야 하며 다음 스키마를 따르세요:
{
  "scenes": [
    {
      "scene_id": int,
      "scene_kr": "한국어 1줄 장면 설명",
      "prompt_en": "영문 이미지 프롬프트 1줄 (샷·앵글·조명·스타일 포함)"
    }
  ]
}
반드시 4개 장면을 추출하세요.
prompt_en은 반드시 영어로 작성하고, wide shot/medium shot/close-up 중 하나, eye-level/low/high angle 중 하나, soft/rim/backlit lighting 중 하나를 포함하세요.
# 여기에 일관성 어휘 가이드를 추가해요 (예: watercolor diary illustration 스타일 유지)
"""  # <- 학생이 스타일 어휘·캐릭터 일관성 가이드 추가
```

작성할 때는 세 가지를 분명히 넣습니다.

- 최상위 키는 반드시 `scenes`
- 장면 수는 반드시 4개
- `prompt_en`은 반드시 영어

스타일 어휘는 너무 길게 쓰지 않습니다. 좋은 스타일 어휘는 짧고 반복 가능합니다.

```
watercolor diary illustration, soft pastel palette, cozy everyday mood
```

캐릭터가 있는 일기라면 인물 일관성을 넣습니다.

```
Keep the same main character across all scenes.
```

풍경 중심 일기라면 장소 일관성을 넣습니다.

```
Keep a consistent neighborhood diary mood across all scenes.
```

나의 스타일 가이드:

| 항목 | 내가 쓸 문장 |
|---|---|
| 화풍 | (학생이 채워요) |
| 색감 | (학생이 채워요) |
| 인물 또는 장소 일관성 | (학생이 채워요) |
| 피하고 싶은 표현 | (학생이 채워요) |

시스템 프롬프트는 길수록 좋은 것이 아닙니다.  
오늘은 스키마, 장면 수, 영어 조건, 스타일 조건만 정확히 넣습니다.

---

## 3. agents/scene.py 함수 골격 작성 (15분)

🎯 **학생 행동**: `agents/__init__.py` 빈 파일 생성 + `agents/scene.py` 새로 작성, 함수 3개 골격을 완성합니다.

먼저 폴더를 만듭니다.

```bash
mkdir -p agents
```

`agents/__init__.py`는 빈 파일로 둡니다.

```bash
touch agents/__init__.py
```

이 파일이 있어야 Python이 `agents` 폴더를 패키지처럼 인식합니다.

이제 `agents/scene.py`를 만듭니다.  
아래 코드는 완성 코드가 아니라 골격입니다.  
`# 여기에 ... 채워요`라고 적힌 부분을 직접 채웁니다.

```python
# agents/scene.py — OpenAI Chat JSON 모드로 일기→scenes JSON 추출
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = ""  # ← §2에서 작성한 시스템 프롬프트를 여기에 채워요


def extract_scenes(diary_text: str) -> list[dict]:
    """일기 텍스트를 받아 scenes 리스트를 반환합니다."""
    # 여기에 OpenAI() 클라이언트 생성 코드를 채워요.
    # 힌트: api_key = os.getenv("OPENAI_API_KEY"), client = OpenAI(api_key=api_key)

    # 여기에 client.chat.completions.create(
    #   model="gpt-4o-mini",
    #   messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": diary_text}],
    #   response_format={"type": "json_object"},
    #   temperature=0.7,
    #   max_tokens=1500,
    # ) 호출 코드를 채워요.

    # 여기에 json.loads(response.choices[0].message.content)["scenes"] 반환 코드를 채워요.
    scenes: list[dict] = []
    return scenes


def validate_scenes(scenes: list[dict]) -> list[str]:
    """scenes 리스트가 4장면 × 필수 3필드(scene_id, scene_kr, prompt_en) 충족하는지 검증합니다."""
    # 여기에 len(scenes) == 4 검증 코드를 채워요. 틀리면 errors에 오류 메시지를 추가해요.
    # 여기에 각 scene에 필수 필드(scene_id, scene_kr, prompt_en)가 있는지 검증 코드를 채워요.
    errors: list[str] = []
    return errors


def save_scenes(scenes: list[dict], out_path: str) -> None:
    """scenes 리스트를 JSON 파일로 저장합니다."""
    # 여기에 Path(out_path).parent.mkdir(parents=True, exist_ok=True) + json.dump 코드를 채워요.
    # 힌트: json.dump({"scenes": scenes}, f, ensure_ascii=False, indent=2)
    pass
```

함수 역할을 분리하는 이유는 다음과 같습니다.

| 함수 | 역할 |
|---|---|
| `extract_scenes` | OpenAI Chat JSON 모드로 일기에서 장면을 추출한다. |
| `validate_scenes` | 장면 수와 필수 필드가 맞는지 확인한다. |
| `save_scenes` | 검증된 장면을 JSON 파일로 저장한다. |

오늘의 성공 기준은 함수가 많아 보이는 것이 아닙니다.  
입력, 검증, 저장이 서로 섞이지 않는 것입니다.

API 키는 코드에 직접 쓰지 않습니다. `.env` 파일에만 둡니다.

```
OPENAI_API_KEY=sk-...
```

코드에는 키 원문이 없어야 합니다. `.gitignore`에 `.env`가 들어 있는지도 확인합니다.

---

## 4. day3_self1.py 시범 호출 작성 (10분)

🎯 **학생 행동**: `day3_self1.py`를 새로 작성합니다. 이 파일은 `agents/scene.py`가 제대로 작동하는지 확인하는 실행 파일입니다.

흐름은 네 단계입니다.

```
diary.md 읽기
  → extract_scenes()
  → validate_scenes()
  → save_scenes()
```

아래 골격을 사용합니다.

```python
# day3_self1.py — agents/scene.py 시범 호출
from pathlib import Path
from agents.scene import extract_scenes, save_scenes, validate_scenes

# 여기에 diary.md를 읽는 코드를 채워요.
# 힌트: diary_text = Path("diary.md").read_text(encoding="utf-8")

# diary.md가 없으면 아래 예제 일기를 사용해도 돼요.
diary_text = ""  # ← diary.md 내용을 여기에 채워요

print("[1] 장면 추출 중...")
scenes = extract_scenes(diary_text)
print(f"  → {len(scenes)}개 장면 추출 완료")

print("[2] 장면 검증 중...")
errors = validate_scenes(scenes)
if errors:
    # 여기에 오류 목록 출력 + 프로그램 종료 코드를 채워요.
    pass
else:
    print("  → 검증 통과")

print("[3] scene_extracted.json 저장 중...")
# 여기에 save_scenes(scenes, "scene_extracted.json") 호출 코드를 채워요.
print("  → 저장 완료")

print("[완료] Day 3 self2의 agents/image.py에서 scene_extracted.json을 입력으로 사용할 수 있어요.")
```

`diary.md`가 있으면 실제 일기를 사용합니다.  
`diary.md`가 없으면 짧은 예제 일기로 먼저 흐름을 확인해도 됩니다.  
예제 일기는 4장면으로 나뉠 수 있어야 합니다.

예시 소재:

```
비 오는 아침 버스를 기다렸다.
작은 카페에 들어가 따뜻한 라떼를 마셨다.
창가에서 낡은 지도를 발견했다.
비가 그치자 다음 여행지를 떠올렸다.
```

이 예시는 그대로 베끼기보다 구조만 참고합니다.  
일기가 너무 짧으면 모델이 4장면을 만들기 어려울 수 있습니다.  
그럴 때는 장소, 행동, 발견, 감정 변화를 한 문장씩 넣습니다.

---

## 5. 실행하고 결과 확인 (5분)

🎯 **학생 행동**: `python day3_self1.py`를 실행한 뒤 `scene_extracted.json` 4장면을 확인하고 Day 2 self2 결과와 비교합니다.

실행 명령:

```bash
python day3_self1.py
```

성공하면 다음 흐름이 보입니다.

```
[1] 장면 추출 중...
[2] 장면 검증 중...
[3] scene_extracted.json 저장 중...
[완료] Day 3 self2의 agents/image.py에서 scene_extracted.json을 입력으로 사용할 수 있어요.
```

결과 파일을 확인합니다.

```bash
python -m json.tool scene_extracted.json
```

확인할 포인트는 네 가지입니다.

- 최상위 키가 `scenes`인가?
- 장면이 4개인가?
- 각 장면에 `scene_id`, `scene_kr`, `prompt_en`이 있는가?
- `prompt_en`이 영어이고 shot, angle, lighting, style 단어를 포함하는가?

Day 2 self2에서 사람이 직접 작성한 `scene_prompts.json`과 비교합니다.

| 항목 | scene_prompts.json (사람) | scene_extracted.json (GPT) |
|---|---|---|
| 장면 1 scene_kr | (학생) | (학생) |
| 장면 1 prompt_en | (학생) | (학생) |
| 샷·앵글·조명 어휘 | (학생) | (학생) |
| 더 풍부한 쪽 | (학생 판단) | |

비교할 때 정답 찾기처럼 보지 않습니다.

- 사람이 쓴 프롬프트는 의도가 분명할 수 있습니다.
- GPT가 쓴 프롬프트는 표현이 풍부할 수 있습니다.

오늘의 목표는 어느 쪽이 완벽한지 고르는 것이 아닙니다.  
자동 추출 결과가 Day 3 self2 이미지 생성 입력으로 쓸 수 있을 만큼 안정적인지 보는 것입니다.

---

## 6. dev_log + Day 3 self2 입력 자료 검증 (3분)

🎯 **학생 행동**: `dev_log.md`에 오늘 작업을 1~2줄 이어 쓰고, `agents/scene.py`가 Day 3 self2의 `agents/image.py`에서 호출 가능한지 확인합니다.

`dev_log.md`에 이어 씁니다.

```markdown
## Day 3 self1
- agents/scene.py로 diary.md에서 4장면 scenes JSON을 추출했다.
- scene_extracted.json을 Day 3 self2 이미지 생성 입력으로 사용할 준비를 했다.
```

Day 3 self2 연결 안내:

> Day 3 self2에서는 `agents/image.py`가 `scene_extracted.json`을 읽어 4장 자동 생성합니다.  
> 본 self1의 `extract_scenes` 함수가 정상 동작해야 합니다.

연결 확인은 import로 합니다.

```python
# 연결 확인 (터미널에서 실행)
from agents.scene import extract_scenes, validate_scenes, save_scenes
print("agents/scene.py import 성공 — Day 3 self2 연결 준비 완료")
```

터미널에서 한 줄 실행하려면 다음처럼 입력해도 됩니다.

```bash
python -c "from agents.scene import extract_scenes, validate_scenes, save_scenes; print('agents/scene.py import 성공 — Day 3 self2 연결 준비 완료')"
```

- 이 확인은 API를 호출하지 않습니다. 그래서 비용이 들지 않습니다.
- import가 실패하면 이미지 생성 단계로 넘어가지 않습니다.

---

## 7. 자기 점검 (10분)

아래 항목을 하나씩 확인합니다.

- [ ] `agents/__init__.py` 빈 파일이 있어요.
- [ ] `agents/scene.py`에 `extract_scenes`, `validate_scenes`, `save_scenes` 3개 함수가 있어요.
- [ ] `SYSTEM_PROMPT`에 JSON 스키마 + 4장면 요구 + `prompt_en` 영어 조건이 있어요.
- [ ] `.env`에 `OPENAI_API_KEY`가 있고 코드에 키 원문이 없어요.
- [ ] `response_format={"type": "json_object"}`가 호출에 포함돼요.
- [ ] `validate_scenes`가 4장면 × 3필드 검증을 해요.
- [ ] `scene_extracted.json`이 생성됐어요.
- [ ] Day 2 self2 `scene_prompts.json`과 비교 표를 채웠어요.
- [ ] `dev_log.md`를 이어썼어요.
- [ ] `agents/scene.py` import가 정상 동작해요 (Day 3 self2 연결 준비).

**Day 3 self2 미리보기**: `agents/image.py` + `scene_extracted.json` 입력 → 4장 자동 생성

자기 점검은 통과 표시만 하는 시간이 아닙니다.  
체크가 비어 있는 항목은 다음 실습의 오류 원인이 됩니다.  
특히 `scene_extracted.json`과 import 성공은 Day 3 self2의 시작 조건입니다.

---

## 흔한 오류 & 해결

| 오류 | 원인 | 해결 |
|---|---|---|
| `JSONDecodeError` | `response_format` 누락 또는 `SYSTEM_PROMPT`에 JSON 지시 없음 | `response_format={"type": "json_object"}` 추가 + "반드시 JSON 객체" 문장 추가 |
| `len(scenes) != 4` | 시스템 프롬프트에 "반드시 4개 장면" 지시가 약함 | "반드시 4개 장면을 추출하세요"를 명시하고 일기를 4개 사건으로 보강 |
| `KeyError: 'scenes'` | 모델이 최상위 키를 `scene_list`나 `data`로 만들었음 | 시스템 프롬프트에 최상위 키는 `"scenes"`라고 명시 |
| `ModuleNotFoundError: agents` | `agents/__init__.py` 누락 또는 실행 위치가 `picture_diary`가 아님 | `agents/__init__.py` 생성 + `picture_diary` 폴더에서 실행 |
| `AuthenticationError` | `.env` 위치가 다르거나 `OPENAI_API_KEY` 변수명이 틀림 | `.env`를 실행 폴더에 두고 변수명을 정확히 확인 |
| `prompt_en`이 한국어로 나옴 | 영어 조건이 시스템 프롬프트에서 약함 | `prompt_en must be written in English` 조건을 추가 |
| 결과 파일이 저장되지 않음 | `save_scenes()` 호출을 빼먹었거나 저장 경로 부모 폴더가 없음 | `save_scenes(scenes, "scene_extracted.json")` 호출 확인 |

오류를 고칠 때는 한 번에 하나만 바꿉니다.  
여러 부분을 동시에 바꾸면 어떤 수정이 효과가 있었는지 알기 어렵습니다.

---

## 📁 산출물 파일 구조

최종 폴더 구조는 다음과 같습니다.

```
picture_diary/
├── agents/
│   ├── __init__.py               # 빈 파일 (새로 작성)
│   └── scene.py                  # 새로 작성 — extract_scenes + validate_scenes + save_scenes
├── day3_self1.py                 # 새로 작성 — agents/scene.py 시범 호출
├── scene_extracted.json          # 자동 추출된 4장면 JSON
├── dev_log.md                    # 이어쓰기
└── scene_prompts.json            # Day 2 self2 산출물 (비교용)
```

각 파일의 역할은 아래와 같습니다.

| 파일 | 역할 |
|---|---|
| `agents/__init__.py` | Python 패키지 인식용 빈 파일 |
| `agents/scene.py` | 일기 → scenes JSON 추출·검증·저장 |
| `day3_self1.py` | `agents/scene.py` 시범 호출 실행 파일 |
| `scene_extracted.json` | 자동 추출된 4장면 JSON (Day 3 self2 입력) |

`scene_extracted.json`은 오늘 실습의 끝이면서 다음 실습의 시작입니다.  
파일 이름을 바꾸지 않습니다. Day 3 self2에서 같은 이름으로 읽을 예정입니다.

---

## 🛡️ 안전 수칙 + 비용 가드

- API 키는 `.env`에만 둡니다. `python-dotenv`로만 로드합니다.
- 코드에 `sk-`로 시작하는 키 원문을 쓰지 않습니다.
- AI 코딩 도우미나 채팅창에 API 키 원문을 입력하지 않습니다.
- `.gitignore`에 `.env`가 있는지 확인합니다.
- `os.environ["OPENAI_API_KEY"] = "sk-..."`처럼 코드에서 직접 설정하지 않습니다.

오늘은 이미지 API를 호출하지 않습니다. 오늘 호출하는 것은 Chat Completions입니다.

**gpt-4o-mini 비용 감각:**

- 약 $0.0001 / 1k token
- 일기 1편 추출 ≈ $0.001
- Day 3 self1 누적 예상 ≈ $0.001

**비용을 줄이는 방법:**

- 같은 일기로 반복 실행을 많이 하지 않습니다.
- `scene_extracted.json`이 만들어지면 내용을 먼저 눈으로 확인합니다.
- 실패 원인을 고친 뒤 다시 실행합니다.
- import 확인은 API 호출 없이 진행합니다.

안전 수칙의 핵심은 단순합니다.  
**키는 숨기고, 호출은 필요한 만큼만 합니다.**

---

## 30분 룰

30분 이상 막히면 혼자 계속 추측하지 않습니다.  
아래 P3 프롬프트 카드를 강사에게 보여주세요.

```
Day 3 self1에서 agents/scene.py를 만들고 있어요.
목표는 diary.md를 읽어 4장면 × scene_id/scene_kr/prompt_en JSON을 만드는 것입니다.
현재 막힌 위치: [에러 메시지 또는 코드 위치]
API 키 원문은 공유하지 않겠습니다.
Q14 환경: uv, Python 3.11+, python-dotenv, openai
```

강사에게 보여줄 때는 세 가지를 같이 준비합니다.

- 실행한 명령
- 나온 오류 메시지
- 현재 `SYSTEM_PROMPT`에서 JSON 조건을 적은 부분

API 키 원문은 절대 보여주지 않습니다.  
화면 공유 중이라면 `.env` 파일을 열지 않습니다.

오늘의 종료 조건은 다음 네 가지입니다.

1. `agents/scene.py` 3개 함수가 있다.
2. `day3_self1.py`로 추출 흐름을 호출한다.
3. `scene_extracted.json`에 4장면이 있다.
4. Day 3 self2에서 import할 준비가 되었다.
