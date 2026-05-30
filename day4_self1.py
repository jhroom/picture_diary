# day4_self1.py — Kling 영상 submit 1회 시범
from pathlib import Path

import fal_client

from agents.video import submit_kling

IMAGE_PATH = Path("outputs") / "2026-05-28" / "scene_1.png"
# 여기에 image_path를 fal.ai 임시 URL로 업로드하는 코드를 채워요.
# 힌트: fal_client.upload_file(str(IMAGE_PATH))는 fal.ai 임시 URL을 반환.

PROMPT = "slow zoom in, cinematic"  # 여기에 day4-s2에서 본 카메라 워크 어휘를 채워요.

temp_url = fal_client.upload_file(str(IMAGE_PATH))

task_id = submit_kling(temp_url, PROMPT, 5)

Path("kling_task_id.txt").write_text(task_id)
print(f"task_id 저장 완료: {task_id}")
