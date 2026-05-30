# Day 4 self2: Kling status 폴링 + picture_diary_pipeline() — 실습가이드 (60분)

Block self-A 종료 (2/2)  
산출 파일: `agents/video.py`(완성), `pipeline.py`, `day4_self2.py`, `outputs/{날짜}/scene_1.mp4`, `results.json`  
핵심 키워드: 비동기 status 폴링, 가드레일 적용, 체이닝, picture_diary_pipeline

---

## 세션 개요

| 항목 | 내용 |
|---|---|
| 시간 | 17:00~17:50 + 자기 점검 10분 |
| 연결 | Day 4 self1 → self2 → Day 5 self1 |
| 마일스톤 | Kling 영상 status 폴링 루프 완성 + `pipeline()` 골격 |
| 비용 | 추가 호출 없음 (self1에서 submit한 task 폴링만) |

오늘은 Day 4 self1에서 이미 submit한 Kling task를 끝까지 확인합니다.  
새 영상 생성을 다시 요청하는 시간이 아니라, 이미 만들어진 `task_id`를 추적하는 시간입니다.

따라서 비용을 새로 쓰지 않고 status 조회, 완료 판정, 결과 URL 수신, mp4 저장 흐름을 연습합니다.

마지막에는 Day 3의 장면 추출과 이미지 생성, Day 4의 영상 생성을 하나의 함수 골격으로 묶습니다.  
이 함수 이름은 `picture_diary_pipeline()`입니다.  
Day 5 self1에서는 이 함수가 도메인 응용의 출발점이 됩니다.

---

## 1. self1 task_id 확인 + Kling 영상 상태 첫 조회 (5분)

🎯 **학생 행동**: `kling_task_id.txt`에 저장된 `task_id`를 읽고 Kling status를 1회 조회합니다.

먼저 터미널 위치를 확인합니다.

```bash
cd picture_diary
```

현재 폴더에 다음 파일이 있어야 합니다.

```
kling_task_id.txt
agents/video.py
guardrails.py
```

`kling_task_id.txt`는 Day 4 self1에서 `submit_kling()`이 반환한 `request_id`를 저장한 파일입니다.  
파일 안에는 긴 문자열 한 줄만 있어야 합니다.

확인 명령은 다음과 같습니다.

```bash
cat kling_task_id.txt
```

값이 비어 있으면 self1의 submit 단계가 끝나지 않은 상태입니다.  
값이 있으면 아래 코드를 `day4_self2.py` 상단에 작성합니다.

```python
# day4_self2.py — 상태 첫 조회
from pathlib import Path
import fal_client

task_id = Path("kling_task_id.txt").read_text().strip()
print(f"self1에서 받은 task_id: {task_id}")

KLING_MODEL = "fal-ai/kling-video/v1/standard/image-to-video"
# 여기에 fal_client.status(KLING_MODEL, task_id, with_logs=False)를 호출하고
# status 객체와 status 문자열을 출력하는 코드를 채워요.
```

실행합니다.

```bash
python day4_self2.py
```

출력에서 확인할 것은 두 가지입니다.

- `task_id`가 빈 문자열이 아닌가?
- `status` 값이 `IN_QUEUE`, `IN_PROGRESS`, `COMPLETED`, `FAILED` 중 하나처럼 보이는가?

---

## 2. agents/video.py status_kling + result_kling 함수 추가 (12분)

🎯 **학생 행동**: self1에서 작성한 `submit_kling()` 아래에 `status_kling()`, `result_kling()` 두 함수를 추가합니다.

열어 볼 파일은 다음입니다.

```
picture_diary/agents/video.py
```

self1에서 이 파일에는 `submit_kling()`만 완성되어 있어야 합니다.  
오늘은 같은 파일에 status 조회와 결과 수신 함수를 붙입니다.

아래 골격을 `submit_kling()` 아래에 그대로 추가한 뒤 빈 부분을 채웁니다.

```python
# agents/video.py (이어쓰기 — submit_kling 아래에 추가)

def status_kling(request_id: str) -> str:
    """Kling status 1회 조회. 상태 문자열 반환."""
    # 여기에 fal_client.status_async(KLING_MODEL, request_id, with_logs=False)를 호출하고
    #   status 객체의 status 필드(예: "IN_PROGRESS", "COMPLETED")를 반환하는 코드를 채워요.
    return ""


def result_kling(request_id: str) -> str:
    """Kling 완료된 영상 결과 받기. 영상 URL 반환."""
    # 여기에 fal_client.result_async(KLING_MODEL, request_id)를 호출하고
    #   result["video"]["url"]을 반환하는 코드를 채워요.
    # 힌트: Kling 응답 구조는 result["video"]["url"] (DALL-E·FLUX와 다름).
    return ""
```

`status` 값은 보통 다음 흐름 중 하나로 관찰됩니다.

| 상태값 | 의미 | 다음 행동 |
|---|---|---|
| `IN_QUEUE` | 대기열에 있음 | 조금 기다린 뒤 다시 조회 |
| `IN_PROGRESS` | 생성 중 | 폴링 계속 |
| `COMPLETED` | 생성 완료 | `result` 호출 가능 |
| `FAILED` | 실패 | 로그 확인 후 중단 |

SDK나 모델 버전에 따라 완료 문자열 표기가 다르게 보일 수 있습니다.  
그래서 뒤에서 `check_predicate(status)`를 사용해 완료 판정을 한 곳에 모읍니다.

---

## 3. 가드레일 4종 + status 폴링 루프 (15분)

🎯 **학생 행동**: `day4_self2.py`에서 `guardrails.py`의 4종 가드를 적용해 status 폴링 루프를 작성합니다.

오늘 사용할 가드는 다음 네 가지입니다.

| 함수 | 목적 | 사용 위치 |
|---|---|---|
| `check_max_iter(iteration)` | 반복 횟수 제한 | while 시작 부분 |
| `check_timeout(start_ts)` | 전체 대기 시간 제한 | while 시작 부분 |
| `check_predicate(status)` | 완료 판정 | status 조회 직후 |
| `check_budget(...)` | 비용 정책 확인 | 루프 시작 전 또는 실행 기록 |

이번 self2는 새 submit을 하지 않으므로 추가 Kling 생성 비용은 없습니다.  
그래도 `check_budget`을 import하고, 비용 가드를 기록해 둡니다.

아래 골격을 `day4_self2.py`에 작성합니다.

```python
# day4_self2.py — status 폴링 + 영상 다운로드
import time, requests
from pathlib import Path
from agents.video import status_kling, result_kling
from guardrails import check_max_iter, check_timeout, check_predicate, check_budget

task_id = Path("kling_task_id.txt").read_text().strip()

iteration = 0
start_ts = time.time()
status = ""

while True:
    # 여기에 4종 가드 적용 (check_max_iter(iteration) and check_timeout(start_ts) 모두 True면 계속,
    # 아니면 break)을 채워요.
    # 힌트: if not (check_max_iter(iteration) and check_timeout(start_ts)): print("[가드 발동] 중단") → break

    status = status_kling(task_id)
    print(f"[{iteration}] status: {status}")

    # 여기에 check_predicate(status)가 True면 break (완료 도달)를 채워요.

    iteration += 1
    time.sleep(5)  # 5초 간격 폴링

# 여기에 status가 "COMPLETED" 또는 "succeeded"일 때 result_kling으로 영상 URL을 받고
#   outputs/{오늘 날짜}/scene_1.mp4로 저장하는 코드를 채워요.
# 힌트: requests.get(video_url).content를 파일에 write.
```

저장 경로는 오늘 날짜 폴더입니다. 예시는 다음과 같습니다.

```
outputs/2026-05-21/scene_1.mp4
```

날짜는 실행일 기준으로 달라질 수 있습니다.  
폴더가 없으면 코드에서 만들어야 합니다.

저장 후에는 파일 크기를 확인합니다.

```bash
ls -lh outputs/*/scene_1.mp4
```

---

## 4. picture_diary_pipeline() 체이닝 골격 (10분)

🎯 **학생 행동**: `pipeline.py` 새 파일을 만들고 4단계 체이닝 함수 골격을 작성합니다.

새 파일 위치는 다음입니다.

```
picture_diary/pipeline.py
```

이 파일은 Day 3과 Day 4의 기능을 연결하는 중심 함수입니다.  
입력은 일기 텍스트입니다.  
출력은 장면 목록, 이미지 경로, 선택적으로 영상 경로가 담긴 `dict`입니다.

아래 골격을 그대로 옮긴 뒤 각 단계의 빈 부분을 채웁니다.

```python
# pipeline.py — 그림일기 통합 파이프라인
import json
from datetime import date
from pathlib import Path
from agents.scene import extract_scenes      # Day 3 self1
from agents.image import batch_generate     # Day 3 self2
from agents.video import submit_kling, status_kling, result_kling


def picture_diary_pipeline(diary_text: str, model: str = "flux", animate_first: bool = True) -> dict:
    """그림일기 통합 파이프라인. diary 텍스트 → scenes → images → (선택) 첫 장면 영상 → results.json."""
    today = date.today().isoformat()
    out_dir = Path("outputs") / today
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) 여기에 scenes = extract_scenes(diary_text) 호출 + 결과 출력 코드를 채워요.

    # 2) 여기에 image_paths = batch_generate(scenes, model, out_dir) 호출 코드를 채워요.

    # 3) (animate_first=True일 때) 여기에 image_paths[0]을 fal.ai에 업로드 + submit_kling 호출
    #    + 폴링 루프 + result_kling으로 영상 URL → 저장 코드를 채워요.
    #    힌트: Day 4 self2 §3 폴링 루프 패턴을 그대로 함수 내부에 흡수.

    # 4) 여기에 results.json에 메타데이터(diary 첫 줄, scenes, image_paths, video_path)를 저장 코드를 채워요.

    return {"scenes": [], "images": [], "video": None}
```

이 함수의 네 단계는 고정합니다.

| 단계 | 입력 | 출력 |
|---|---|---|
| scene | `diary_text` | `scenes` |
| image | `scenes` | `image_paths` |
| video | `image_paths[0]` | `scene_1.mp4` |
| results | 전체 메타데이터 | `results.json` |

`results.json`에는 최소한 다음 정보가 들어가야 합니다.

```json
{
  "diary_first_line": "...",
  "scenes": [],
  "images": [],
  "video": null
}
```

---

## 5. day4_self2.py에서 pipeline 첫 시범 실행 (5분)

🎯 **학생 행동**: `picture_diary_pipeline()`을 1회 호출합니다.

처음 실행은 비용 절약을 위해 `animate_first=False`로 시작합니다.

`day4_self2.py` 하단에 아래 골격을 추가합니다.

```python
# day4_self2.py 하단에 추가
from pipeline import picture_diary_pipeline
from pathlib import Path

diary_text = Path("diary.md").read_text(encoding="utf-8")

# 여기에 picture_diary_pipeline(diary_text, animate_first=False)를 호출하고
# 결과를 출력하는 코드를 채워요.
```

실행 전 확인할 파일은 다음입니다.

```
diary.md
agents/scene.py
agents/image.py
agents/video.py
pipeline.py
```

`diary.md`가 없으면 Day 3에서 사용한 일기 텍스트 파일을 같은 이름으로 둡니다.

실행합니다.

```bash
python day4_self2.py
```

`results.json`을 확인합니다.

```bash
python -m json.tool results.json
```

---

## 6. dev_log + Day 5 입력 자료 검증 (3분)

🎯 **학생 행동**: 오늘 배운 비동기 폴링 패턴과 pipeline 인터페이스를 짧게 기록합니다.

`dev_log.md`에 아래 두 줄을 본인 말로 남깁니다.

```markdown
## Day 4 self2

- Kling은 submit 직후 URL을 주지 않으므로 status 폴링 후 result를 받아야 한다.
- picture_diary_pipeline(diary_text, model, animate_first)는 scene→image→video→results 흐름을 묶는 인터페이스다.
- 내일 Day 5 self1에서는 이 pipeline()을 도메인 응용(제품·이모티콘·여행 중 1개 선택)에 적용하고, cost_report.md로 Day 1~4 누적 비용을 추적한다.
```

다음 파일이 있는지 확인합니다.

```bash
ls agents/video.py pipeline.py day4_self2.py results.json
```

영상이 완료되었다면 아래 파일도 확인합니다.

```bash
ls outputs/*/scene_1.mp4
```

이 단계에서는 새 API 호출을 만들지 않습니다.  
기록과 입력 자료 점검만 합니다.

---

## 7. 자기 점검 (10분)

아래 항목을 차례대로 확인합니다.

- [ ] `kling_task_id.txt`에서 `task_id`를 읽어 status를 1회 조회할 수 있다.
- [ ] `agents/video.py`에 `status_kling`, `result_kling` 함수가 추가되었다.
- [ ] 폴링 루프에서 `check_max_iter`, `check_timeout`, `check_predicate` 3종을 모두 사용한다.
- [ ] 폴링 완료 후 `scene_1.mp4` 파일이 `outputs/{날짜}/` 폴더에 저장된다.
- [ ] `pipeline.py`에 `picture_diary_pipeline()` 함수 골격이 있고 4개 주석이 채워져 있다.
- [ ] `animate_first=False`로 `pipeline()`을 1회 호출했을 때 `results.json`이 생성된다.
- [ ] `results.json`에 `scenes`, `images`, `video` 키가 있다.
- [ ] `dev_log.md`에 비동기 폴링 패턴을 1줄 이상 적었다.
- [ ] Day 5 self1에서 사용할 도메인 후보를 하나 떠올렸다.

**Day 5 self1 미리보기:**  
내일 Day 5 self1에서는 오늘 완성한 `picture_diary_pipeline()`을 도메인 응용에 적용한다.  
제품 홍보·이모티콘·여행 기록 중 하나를 골라 `pipeline()`을 호출하고,  
`cost_report.md`로 Day 1~4 누적 비용을 추적한다.

---

## 흔한 오류 & 해결

| 오류 | 증상 | 해결 |
|---|---|---|
| `status_async`와 `status` 혼동 | 함수 이름을 잘못 써서 `AttributeError`가 난다. | 현재 사용 중인 SDK 문서와 수업 코드의 함수명을 맞춘다. |
| `result["video"]["url"]` 접근 오류 | `result.video.url`처럼 속성 접근을 시도한다. | Kling 응답은 dict 구조로 보고 대괄호 접근을 사용한다. |
| 폴링 루프 무한 실행 | 터미널이 계속 status만 출력한다. | `check_max_iter`, `check_timeout`, `check_predicate` 위치를 확인한다. |
| `agents` 모듈 import 오류 | `from agents.video import ...`에서 실패한다. | 터미널 위치를 `picture_diary` 루트로 맞추고 실행한다. |

`result_kling()`은 완료 후에만 호출합니다.  
완료 전 `result`를 호출하면 빈 결과나 오류가 날 수 있습니다.

---

## 📁 산출물 파일 구조

오늘이 끝나면 `picture_diary/` 아래 구조가 다음처럼 보입니다.

```
picture_diary/
├── agents/video.py          # self1 submit + 본 self2에서 status_kling, result_kling 추가
├── pipeline.py              # 새로 작성 — picture_diary_pipeline() (4단계: scene→image→video→results.json)
├── day4_self2.py            # 새로 작성 — status 폴링 + 영상 다운로드 + pipeline 시범 실행
├── outputs/{날짜}/
│   └── scene_1.mp4
└── results.json
```

---

## 🛡️ 안전 수칙 + 비용 가드

Kling `submit`은 비용이 발생합니다.  
Day 4 self1에서 1회 submit한 비용은 대략 $0.20 수준입니다.  
Day 4 self2는 기존 task를 폴링하므로 추가 영상 생성 비용이 없습니다.

다만 실수로 `submit_kling()`을 반복 호출하면 새 비용이 발생합니다.  
오늘의 기본 실행에서는 `animate_first=False`로 pipeline을 호출합니다.  
이 설정은 추가 Kling submit을 막기 위한 비용 가드입니다.

---

## 30분 룰

같은 지점에서 30분 이상 막히면 강사나 조교에게 질문합니다.  
질문할 때는 다음 네 가지를 함께 보여 줍니다.

- 실행한 명령
- 터미널 출력
- 현재 작성한 함수 이름
- 최종 `status` 값

질문 예시는 다음과 같습니다.

```
day4_self2.py에서 status는 IN_PROGRESS로 나오지만 10회 이후에도 완료되지 않습니다.
check_max_iter와 check_timeout은 적용했습니다.
task_id와 status 출력은 첨부했습니다.
다음 확인 위치를 알고 싶습니다.
```

30분 룰은 포기 규칙이 아닙니다.  
잘못된 방향으로 오래 머무르지 않기 위한 협업 규칙입니다.

오늘의 멈춤 기준은 분명합니다.  
status 폴링 흐름이 있고, 완료 시 `mp4` 저장 경로가 있으며, `pipeline` 골격이 만들어져 있으면 다음 단계로 넘어갈 수 있습니다.
