# day3_self1.py — agents/scene.py 시범 호출
from pathlib import Path
from agents.scene import extract_scenes, save_scenes, validate_scenes
import sys

# 여기에 diary.md를 읽는 코드를 채워요.
diary_text = Path("diary.md").read_text(encoding="utf-8")

print("[1] 장면 추출 중...")
scenes = extract_scenes(diary_text)
print(f"  → {len(scenes)}개 장면 추출 완료")

print("[2] 장면 검증 중...")
errors = validate_scenes(scenes)
if errors:
    for err in errors:
            print(f"-> {err}")
    sys.exit(1)
else:
    print("  → 검증 통과")

print("[3] scene_extracted.json 저장 중...")
save_scenes(scenes, "scene_extracted.json")
print("  → 저장 완료")

print("[완료] Day 3 self2의 agents/image.py에서 scene_extracted.json을 입력으로 사용할 수 있어요.")