# Day 4 self1: 비동기 폴링 패러다임 + Kling submit 첫 호출 — 실습가이드 (60분)

Block self-A 시작 (1/2)  
산출 파일: `agents/video.py`(submit 함수), `day4_self1.py`, `kling_task_id.txt`, `guardrails.py`  
핵심 키워드: 비동기 폴링, submit/status/result, 가드레일 4종, task_id

---

## 세션 개요

| 항목 | 내용 |
|---|---|
| 세션 ID | day4-self1 |
| 오늘 목표 | Day 3에서 만든 `scene_1.png`를 Kling Image-to-Video 작업으로 제출하고 `task_id`를 보관한다. |
| 입력 파일 | `picture_diary/outputs/{날짜}/scene_1.png` |
| 만드는 파일 | `picture_diary/agents/video.py`, `picture_diary/day4_self1.py`, `picture_diary/guardrails.py` |
| 만드는 결과 | `picture_diary/kling_task_id.txt` |
| 하지 않는 일 | 영상 완료 확인, 다운로드, status 반복 조회, 파이프라인 체이닝은 하지 않는다. |
| 다음 연결 | Day 4 self2에서 `kling_task_id.txt`를 읽어 status 폴링 후 result를 받는다. |
| 비용 방향 | Kling 5초 영상은 약 $0.20이며 self1에서는 1장만 submit한다. |
| 안전 방향 | 무한 루프를 피하기 위해 반복 횟수, 시간, 상태, 예산 가드를 먼저 설계한다. |

오늘은 영상을 바로 받는 시간이 아닙니다.  
오늘은 "작업을 맡기고 번호표를 받는 흐름"을 코드로 만드는 시간입니다.

- Day 3 self2에서 만든 이미지는 이미 준비된 입력입니다.
- Day 4 self1은 그 이미지를 Kling에 제출하고 `task_id`를 파일로 남깁니다.
- Day 4 self2는 그 `task_id`를 이용해 진행 상태를 확인합니다.

---

## 1. 비동기 폴링 vs 동기 호출 차이 (8분)

🎯 **학생 행동**: day4-s1 강사 시간에 본 병원 대기표 비유를 다시 떠올리고 1줄 메모

동기 호출은 요청한 자리에서 결과가 돌아올 때까지 기다리는 방식입니다.  
비동기 호출은 요청을 먼저 접수하고, 나중에 상태를 다시 확인하는 방식입니다.

병원 대기표 비유로 보면 다음과 같습니다.

| 비유 | API 용어 | 의미 |
|---|---|---|
| 접수 | `submit` | 작업을 맡긴다. |
| 번호표 | `request_id` 또는 `task_id` | 나중에 조회할 식별자다. |
| 전광판 확인 | `status` | 아직 대기 중인지 확인한다. |
| 진료 완료 | `result` | 최종 결과를 받는다. |

Day 1의 DALL-E 3 호출은 결과 URL이 바로 돌아오는 동기 흐름에 가깝습니다.  
Day 2의 FLUX-schnell `subscribe`는 내부에서 기다려 주기 때문에 겉으로는 동기처럼 보입니다.  
Day 4의 Kling은 `submit`, `status`, `result`를 나누어 생각해야 합니다.

| 모델 | 호출 방식 | 응답 시간 | 결과 받는 법 |
|---|---|---|---|
| DALL-E 3 (Day 1) | 동기 | 5~15초 | 즉시 url |
| FLUX-schnell (Day 2) | subscribe 내부 대기 | 5~30초 | 즉시 url처럼 사용 |
| Kling (Day 4) | submit/status/result | 30초~5분 | task_id로 별도 조회 |

오늘은 Kling의 첫 단계인 `submit`만 작성합니다.  
`status`와 `result`는 self2에서 작성합니다.

아래 한 줄을 본인 말로 채웁니다.

```
동기 호출과 비동기 호출의 차이:
```

메모 예시는 직접 바꾸어 씁니다.

```
동기는 결과를 기다리고, 비동기는 번호표를 받아 나중에 확인한다.
```

오늘 코드의 목표는 "번호표를 잃어버리지 않는 것"입니다.  
그래서 `kling_task_id.txt` 파일 저장이 중요합니다.

---

## 2. 가드레일 4종 설계 (8분)

🎯 **학생 행동**: `guardrails.py`를 새로 만들고 4종 가드 함수 골격 작성

비동기 작업은 기다림이 길어질 수 있습니다.  
기다림이 길어질수록 안전장치가 필요합니다.  
오늘은 실제 폴링 루프를 만들지는 않지만, self2에서 쓸 가드의 모양을 먼저 만듭니다.

가드레일 4종은 다음과 같습니다.

| 가드 | 막는 위험 | 오늘 할 일 |
|---|---|---|
| Max Iter | 끝나지 않는 반복 | 최대 반복 횟수 조건을 만든다. |
| Timeout | 너무 오래 기다림 | 시작 시각 기준 제한 시간을 만든다. |
| Predicate | 상태 문자열 오판 | 완료 상태인지 판단하는 함수를 만든다. |
| Budget Cap | 비용 초과 | 사용 금액이 상한 이하인지 본다. |

프로젝트 폴더로 이동합니다.

```bash
cd picture_diary
```

새 파일 위치는 다음과 같습니다.

```
picture_diary/guardrails.py
```

아래 골격을 입력합니다.

```python
# guardrails.py — 비동기 폴링 4종 가드
import time
from typing import Callable

MAX_ITER = 60
TIMEOUT_SEC = 300
BUDGET_CAP_USD = 0.50


def check_max_iter(iteration: int) -> bool:
    # 여기에 iteration < MAX_ITER 반환 코드를 채워요.
    return True


def check_timeout(start_ts: float) -> bool:
    # 여기에 time.time() - start_ts < TIMEOUT_SEC 반환 코드를 채워요.
    return True


def check_predicate(status: str, accept: tuple = ("completed", "succeeded")) -> bool:
    # 여기에 status.lower() in accept 반환 코드를 채워요.
    return False


def check_budget(used_usd: float) -> bool:
    # 여기에 used_usd < BUDGET_CAP_USD 반환 코드를 채워요.
    return True
```

이 파일은 오늘 당장 긴 루프에 연결하지 않습니다.  
오늘은 함수 이름과 역할을 먼저 고정합니다.  
self2에서 status 폴링을 만들 때 이 함수들이 안전장치가 됩니다.

강사 시간에 본 상수도 함께 기억합니다.

| 상수 | 의미 |
|---|---|
| `MAX_ITERATIONS=12` | 5초 간격으로 최대 12번 확인 |
| `POLL_INTERVAL_SECONDS=5` | 확인 사이의 대기 시간 |
| `TIMEOUT_SECONDS=70` | 전체 대기 상한 |
| `MAX_BUDGET_USD=0.50` | 실습 비용 상한 |

오늘 골격에서는 이름을 짧게 둡니다.  
프로젝트에서 이미 다른 이름을 쓴다면 기존 이름에 맞춰도 됩니다.  
중요한 것은 네 종류의 가드가 모두 분리되어 있다는 점입니다.

---

## 3. agents/video.py submit 함수 작성 (15분)

🎯 **학생 행동**: `agents/video.py`를 새로 만들고 `submit_kling()` 함수만 작성

오늘 만드는 `video.py`는 영상 생성 API 전용 파일입니다.  
Day 3의 `agents/image.py`가 이미지 생성을 담당했다면, Day 4의 `agents/video.py`는 영상 작업을 담당합니다.

먼저 폴더를 확인합니다.

```bash
ls agents
```

`scene.py`와 `image.py`가 보이면 Day 3 흐름이 이어진 것입니다.

새 파일 위치는 다음과 같습니다.

```
picture_diary/agents/video.py
```

오늘은 `submit_kling()`만 작성합니다. 아래 골격을 입력합니다.

```python
# agents/video.py — Kling Image-to-Video 비동기 호출
import os
from dotenv import load_dotenv
import fal_client

load_dotenv()

KLING_MODEL = "fal-ai/kling-video/v2/master/image-to-video"  # 강사 day4-s3 시연 엔드포인트 일치


def submit_kling(image_url: str, prompt: str, duration: int = 5) -> str:
    # 여기에 fal_client.submit(KLING_MODEL, arguments={...})를 호출하고
    #   handler.request_id를 반환하는 코드를 채워요.
    # 힌트: arguments = {"image_url": image_url, "prompt": prompt, "duration": duration}
    # 힌트: submit은 즉시 반환하고 영상은 백그라운드에서 생성됩니다.
    return ""


# status_kling, result_kling 함수는 self2에서 작성
```

`submit_kling()`의 입력은 세 가지입니다.

| 입력 | 의미 |
|---|---|
| `image_url` | fal.ai가 접근할 수 있는 이미지 URL |
| `prompt` | 영상 움직임을 설명하는 문장 |
| `duration` | 영상 길이, 오늘은 5초 |

주의할 점은 `image_url`입니다.  
Kling에는 내 컴퓨터의 로컬 파일 경로를 그대로 넘기지 않습니다.  
먼저 `fal_client.upload_file()`로 임시 URL을 만든 뒤 넘깁니다.

- `submit_kling()` 안에서는 이미 URL이 들어온다고 가정합니다.
- 업로드는 다음 단계의 `day4_self1.py`에서 처리합니다.

오늘 `video.py`에 `status_kling()`이나 `result_kling()`을 미리 만들 필요는 없습니다.  
그 둘은 Day 4 self2의 범위입니다.

---

## 4. day4_self1.py 실행 + task_id 보관 (8분)

🎯 **학생 행동**: `outputs/{날짜}/scene_1.png`를 Kling에 submit하고 `kling_task_id.txt`에 저장

이제 실행 파일을 만듭니다. 새 파일 위치는 다음과 같습니다.

```
picture_diary/day4_self1.py
```

이 파일은 세 가지 일을 합니다.

| 순서 | 일 |
|---|---|
| 1 | `scene_1.png` 경로를 정한다. |
| 2 | 이미지를 fal.ai 임시 URL로 업로드한다. |
| 3 | Kling에 submit하고 `task_id`를 파일에 저장한다. |

아래 골격을 입력합니다.

```python
# day4_self1.py — Kling 영상 submit 1회 시범
from pathlib import Path

import fal_client

from agents.video import submit_kling

IMAGE_PATH = Path("outputs") / "2026-05-21" / "scene_1.png"
# 여기에 image_path를 fal.ai 임시 URL로 업로드하는 코드를 채워요.
# 힌트: fal_client.upload_file(str(IMAGE_PATH))는 fal.ai 임시 URL을 반환.

PROMPT = ""  # 여기에 day4-s2에서 본 카메라 워크 어휘를 채워요.

# 여기에 submit_kling 호출 + task_id를 kling_task_id.txt에 저장하는 코드를 채워요.
```

`IMAGE_PATH`의 날짜는 본인 결과 폴더에 맞춥니다.

현재 날짜 폴더를 확인합니다.

```bash
ls outputs
```

그 안에 `scene_1.png`가 있는지 확인합니다.

```bash
ls outputs/2026-05-21/scene_1.png
```

날짜가 다르면 `2026-05-21` 부분만 바꿉니다.

프롬프트에는 카메라 움직임을 짧게 씁니다. 예시는 다음과 같습니다.

```
slow zoom in, gentle camera movement, cinematic, soft motion
```

풍경 이미지라면 너무 큰 움직임을 요구하지 않습니다.  
`duration`은 기본값 5초를 그대로 둡니다.

self1은 실습 비용을 줄이기 위해 1장만 submit합니다.  
Kling 5초 영상은 약 $0.20입니다.  
4장을 모두 submit하면 비용과 대기 시간이 늘어납니다.

---

## 5. 실행하고 task_id 확인 (3분)

🎯 **학생 행동**: `python day4_self1.py` 실행 후 `kling_task_id.txt` 생성 확인

터미널 위치가 `picture_diary`인지 확인합니다.

```bash
pwd
```

실행합니다.

```bash
python day4_self1.py
```

성공하면 `kling_task_id.txt`가 생깁니다.

```bash
ls -la kling_task_id.txt
```

내용을 확인합니다.

```bash
cat kling_task_id.txt
```

`task_id`는 UUID처럼 보이거나 `req_`로 시작하는 문자열일 수 있습니다.  
정확한 모양은 실행 환경에 따라 다를 수 있습니다.  
중요한 것은 빈 파일이 아니라는 점입니다.

영상은 아직 생성 중일 수 있습니다.  
오늘은 여기서 영상 URL을 받으려고 하지 않습니다.  
Day 4 self2에서 이 파일을 읽어 status 폴링을 진행합니다.

---

## 6. dev_log.md 이어쓰기 (3분)

🎯 **학생 행동**: 동기 vs 비동기 차이 1줄 + 가드레일 4종 의미 1줄 정리

`dev_log.md`가 이미 있으면 이어 씁니다.  
없으면 새로 만들어도 됩니다. 오늘 남길 기록은 두 줄이면 충분합니다.

```markdown
## Day 4 self1

- 동기 호출은 결과를 바로 기다리고, 비동기 호출은 task_id를 받아 나중에 status/result로 확인한다.
- 가드레일 4종은 반복 횟수, 대기 시간, 완료 조건, 비용 상한을 제한해 무한 대기와 비용 초과를 막는다.
```

아래 명령으로 파일을 엽니다.

```bash
code dev_log.md
```

에디터가 없다면 터미널 편집기나 IDE에서 열어도 됩니다.  
기록에는 API 키나 실제 비밀값을 쓰지 않습니다.  
`task_id`는 실습 기록으로 남길 수 있지만, 공개 저장소에는 올리지 않는 편이 안전합니다.

---

## 7. 자기 점검 (10분)

🎯 **학생 행동**: 파일, 함수, task_id, 다음 연결을 스스로 확인

먼저 파일이 모두 있는지 확인합니다.

```bash
ls -la guardrails.py
ls -la agents/video.py
ls -la day4_self1.py
ls -la kling_task_id.txt
```

다음 체크리스트를 표시합니다.

| 항목 | 확인 |
|---|---|
| `guardrails.py`에 4종 함수가 있다. | [ ] |
| `agents/video.py`에 `submit_kling()`이 있다. | [ ] |
| `submit_kling()`은 `handler.request_id`를 반환하도록 채웠다. | [ ] |
| `day4_self1.py`에서 `fal_client.upload_file()`을 사용했다. | [ ] |
| `PROMPT`가 빈 문자열이 아니다. | [ ] |
| `kling_task_id.txt`가 생성되었다. | [ ] |
| `kling_task_id.txt` 내용이 비어 있지 않다. | [ ] |
| self1에서 1장만 submit했다. | [ ] |

**Day 4 self2 연결 안내:**  
self2에서는 `kling_task_id.txt`의 `task_id`를 읽어 Kling status 폴링을 하고, 완료되면 result로 영상 URL을 받는다.

self2에서 이어질 흐름은 다음과 같습니다.

| self2 작업 | 오늘과의 연결 |
|---|---|
| `status_kling()` 작성 | 오늘 받은 `task_id`를 입력으로 사용 |
| `result_kling()` 작성 | 완료된 작업의 영상 URL 수신 |
| 안전 루프 작성 | 오늘 만든 `guardrails.py` 활용 |
| pipeline 체이닝 | 이미지 4장과 영상 생성 흐름 연결 |

오늘은 "제출"까지가 완료 범위입니다.  
완료 여부 확인과 영상 파일 저장은 다음 세션 범위입니다.

---

## 8. 마무리 정리 (5분)

🎯 **학생 행동**: 오늘 만든 산출물의 역할을 한 문장씩 말해 보기

오늘 만든 파일의 역할을 다시 정리합니다.

| 파일 | 역할 |
|---|---|
| `guardrails.py` | self2 폴링 루프의 안전장치 함수 모음 |
| `agents/video.py` | Kling 영상 작업 제출 함수 |
| `day4_self1.py` | 이미지 업로드, submit 실행, task_id 저장 |
| `kling_task_id.txt` | self2가 이어받을 작업 식별자 |

오늘의 핵심 문장은 다음입니다.

> **비동기 영상 생성은 결과를 바로 받지 않고 task_id를 먼저 저장한다.**

이 문장을 이해했다면 self2의 status 폴링이 훨씬 쉬워집니다.

---

## 흔한 오류 & 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| `ModuleNotFoundError: fal_client` | 패키지가 설치되지 않음 | `uv pip install fal-client`로 설치 |
| `scene_1.png`를 찾을 수 없음 | 날짜 폴더가 다름 | `ls outputs`로 실제 날짜 확인 |
| `task_id` 파일이 비어 있음 | `submit_kling()` 반환값을 저장하지 않음 | 반환값을 변수에 담고 파일에 기록 |
| 로컬 경로를 그대로 넘김 | 업로드 단계를 건너뜀 | `fal_client.upload_file()`로 URL 생성 |
| `PROMPT = ""` 그대로 실행 | 카메라 워크 문장 미작성 | 짧은 움직임 문장을 넣기 |
| 4장을 한 번에 제출 | self1 범위 초과 | 오늘은 `scene_1.png` 1장만 실행 |

오류가 나면 먼저 파일 경로, API 키, 패키지 설치, 프롬프트 빈 문자열 여부를 확인합니다.  
API 호출을 반복하기 전에 비용을 먼저 생각합니다.

---

## 📁 산출물 파일 구조

오늘 세션 뒤의 폴더는 아래 모양에 가까워야 합니다.

```
picture_diary/
├── agents/
│   ├── scene.py
│   ├── image.py
│   └── video.py
├── day4_self1.py
├── kling_task_id.txt
├── guardrails.py
└── outputs/
    └── 2026-05-21/
        ├── scene_1.png
        ├── scene_2.png
        ├── scene_3.png
        └── scene_4.png
```

`outputs` 날짜 폴더는 본인 실행 날짜와 다를 수 있습니다.  
오늘 직접 사용하는 이미지는 `scene_1.png` 한 장입니다.

---

## 🛡️ 안전 수칙 + 비용 가드

Kling 5초 영상은 대략 $0.20입니다.  
self1에서는 1장만 submit하므로 예상 비용은 약 $0.20입니다.  
반복 실행하면 같은 이미지라도 매번 비용이 발생할 수 있습니다.

실패 후 재실행하기 전에는 다음을 확인합니다.

| 확인 | 이유 |
|---|---|
| `IMAGE_PATH`가 맞는가 | 잘못된 파일 제출 방지 |
| `PROMPT`가 비어 있지 않은가 | 의미 없는 작업 방지 |
| `kling_task_id.txt`가 이미 있는가 | 중복 제출 방지 |
| API 키가 설정되어 있는가 | 인증 실패 반복 방지 |
| 오늘은 1장만 제출하는가 | 비용 제한 유지 |

비용 가드는 단순한 돈 문제만이 아닙니다.  
잘못된 루프가 API를 계속 호출하지 않게 만드는 안전장치입니다.

---

## 30분 룰

30분 안에 `task_id`가 나오지 않으면 새 기능을 추가하지 않습니다.  
다음 순서로만 확인합니다.

1. `outputs/{날짜}/scene_1.png` 경로 확인
2. `fal_client` 설치 확인
3. `.env` 또는 환경변수 확인
4. `PROMPT` 빈 문자열 여부 확인
5. `submit_kling()` 반환값 확인
6. `kling_task_id.txt` 저장 위치 확인

여기까지 확인해도 막히면 현재 오류 메시지를 그대로 기록합니다.  
기록할 때는 비밀 키를 지웁니다.

오늘 범위는 제출과 `task_id` 보관입니다.  
영상 완성 확인은 self2에서 진행합니다.
