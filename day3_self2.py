# day3_self2.py
from pathlib import Path
from datetime import date
import json
from agents.image import batch_generate


# 여기에 scene_prompts.json 또는 agents/scene.py 결과를 로드하고
# outputs/{오늘 날짜}/ 폴더에 4장 일괄 생성하는 코드를 채워요.
# 힌트: today = date.today().isoformat() → out_dir = Path("outputs") / today.


today = date.today().isoformat()
out_dir = Path("outputs") / today

with open("scene_extracted.json", encoding="utf-8") as f:
    data = json.load(f)
scenes = data["scenes"]

paths = batch_generate(scenes, model="flux", out_dir=out_dir)
print(paths)
