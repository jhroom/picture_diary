# day4_self2.py — 상태 첫 조회
from pathlib import Path
import fal_client
from dotenv import load_dotenv
import time
from agents.video import status_kling, result_kling
from guardrails import check_max_iter, check_timeout, check_predicate
import datetime
import requests
from datetime import date

from pipeline import picture_diary_pipeline


load_dotenv()

task_id = Path("kling_task_id.txt").read_text().strip()
print(f"self1에서 받은 task_id: {task_id}")

KLING_MODEL = "fal-ai/kling-video/v1/standard/image-to-video"
# 여기에 fal_client.status(KLING_MODEL, task_id, with_logs=False)를 호출하고
# status 객체와 status 문자열을 출력하는 코드를 채워요.

st = fal_client.status(KLING_MODEL, task_id, with_logs=False)
print(f"st : {st}")
print(f"st : {type(st).__name__}")

iteration = 0
start_ts = time.time()
status_name = type(st).__name__

while True:
    if not (check_max_iter(iteration) and check_timeout(start_ts)):
        print("[가드 발동] 중단")
        break

    status = status_kling(task_id)
    print(f"[{iteration}] status: {status}")
    print("name", type(status).__name__)

    if check_predicate(type(status).__name__):
        print("check prediccate true")
        break

    iteration += 1
    time.sleep(5)  # 5초 간격 폴링

# 여기에 status가 "COMPLETED" 또는 "succeeded"일 때 result_kling으로 영상 URL을 받고
#   outputs/{오늘 날짜}/scene_1.mp4로 저장하는 코드를 채워요.
# 힌트: requests.get(video_url).content를 파일에 write

if check_predicate(status_name):
    url = result_kling(task_id)
    today = date.today().isoformat()
    output_dir = Path(f"outputs/{today}")
    output_dir.mkdir(exist_ok=True)
    video_path = output_dir / "scene_1.mp4"
    video_path.write_bytes(requests.get(url).content)



diary_text = Path("diary.md").read_text(encoding="utf-8")

# 여기에 picture_diary_pipeline(diary_text, animate_first=False)를 호출하고
# 결과를 출력하는 코드를 채워요.
result = picture_diary_pipeline(diary_text, animate_first=False)
print(result)