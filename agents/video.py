# agents/video.py — Kling Image-to-Video 비동기 호출
import os
from dotenv import load_dotenv
import fal_client

load_dotenv()

KLING_MODEL = "fal-ai/kling-video/v2/master/image-to-video"


def submit_kling(image_url: str, prompt: str, duration: int = 5) -> str:
    handler = fal_client.submit(
        KLING_MODEL,
        arguments= {
            "image_url": image_url,
            "prompt": prompt,
            "duration": duration
            }
        )
    
    return handler.request_id

def status_kling(request_id: str) -> str:
    """Kling status 1회 조회. 상태 문자열 반환."""

    return fal_client.status(KLING_MODEL, request_id, with_logs=False)

def result_kling(request_id: str) -> str:
    """Kling 완료된 영상 결과 받기. 영상 URL 반환."""
    result = fal_client.result(KLING_MODEL, request_id)

    return result["video"]["url"]
