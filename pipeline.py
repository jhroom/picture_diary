# pipeline.py — 그림일기 통합 파이프라인
import json
import time
import requests
from datetime import date
from pathlib import Path
import fal_client
from agents.scene import extract_scenes
from agents.image import batch_generate
from agents.video import submit_kling, status_kling, result_kling
from guardrails import check_max_iter, check_timeout, check_predicate


def picture_diary_pipeline(diary_text: str, model: str = "flux", animate_first: bool = True) -> dict:
    """그림일기 통합 파이프라인. diary 텍스트 → scenes → images → (선택) 첫 장면 영상 → results.json."""
    today = date.today().isoformat()
    out_dir = Path("outputs") / today
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) 여기에 scenes = extract_scenes(diary_text) 호출 + 결과 출력 코드를 채워요.
    scenes = extract_scenes(diary_text)

    # 2) 여기에 image_paths = batch_generate(scenes, model, out_dir) 호출 코드를 채워요.
    image_paths = batch_generate(scenes, model, out_dir)


    # 3) (animate_first=True일 때) 여기에 image_paths[0]을 fal.ai에 업로드 + submit_kling 호출
    #    + 폴링 루프 + result_kling으로 영상 URL → 저장 코드를 채워요.
    #    힌트: Day 4 self2 §3 폴링 루프 패턴을 그대로 함수 내부에 흡수.
    video_path = None
    if animate_first:
        image_url = fal_client.upload_file(str(image_paths[0]))
        prompt = scenes[0]["prompt_en"]
        request_id = submit_kling(image_url, prompt)

        iteration = 0
        start_ts = time.time()
        status = None
        while True:
            if not (check_max_iter(iteration) and check_timeout(start_ts)):
                print("[가드 발동] 중단")
                break
            status = status_kling(request_id)
            print(f"[{iteration}] status: {type(status).__name__}")
            if check_predicate(type(status).__name__):
                break
            iteration += 1
            time.sleep(5)

        if status and check_predicate(type(status).__name__):
            video_url = result_kling(request_id)
            video_path = out_dir / "scene_1.mp4"
            video_path.write_bytes(requests.get(video_url).content)


    # 4) 여기에 results.json에 메타데이터(diary 첫 줄, scenes, image_paths, video_path)를 저장 코드를 채워요.
    results = {
        "diary_first_line": diary_text.splitlines()[0],
        "scenes": scenes,
        "images": [str(p) for p in image_paths],
        "video": str(video_path),
    }
    (out_dir / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return results