# agents/image.py — DALL-E 또는 FLUX 분기 이미지 생성
import os, requests, json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import fal_client
import base64

load_dotenv()

COMMON_STYLE = "cinematic color, wide shot"  # ← 캐릭터 일관성 어휘 (§2에서 정한 화풍·색·인물 표현 1줄)


def call_dalle(prompt: str, seed: int | None = None) -> str:
    """Dgpt-image-1.5로 1장 생성, URL 반환."""
    client = OpenAI()

    response = client.images.generate(
        model="gpt-image-1.5",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png"
    )

    return response.data[0].b64_json


def call_flux(prompt: str, seed: int = 42) -> str:
    """FLUX로 1장 생성, URL 반환. seed로 일관성 강화."""

    result = fal_client.run(
        "fal-ai/flux/schnell",
        arguments={
            "prompt" : prompt,
            "seed": seed,  #일관성을 위한 시드 고정
            "num_images": 1,
            "image_size": "square_hd"
        }
    )
    return result["images"][0]["url"]


def generate_image(prompt: str, model: str = "gpt", seed: int = 42) -> str:
    """모델 분기 함수. gpt 또는 FLUX 호출."""
    
    if model == "gpt":
        return call_dalle(prompt)
    elif model == "flux": 
        return call_flux(prompt, seed)


def save_image(data: str, out_path: Path, model: str = "flux") -> None:
    if model == "gpt":
        image_bytes = base64.b64decode(data)
        out_path.write_bytes(image_bytes)
    else:
        out_path.write_bytes(requests.get(data).content)


def batch_generate(scenes: list[dict], model: str, out_dir: Path) -> list[Path]:
    """scenes 리스트를 받아 4장 일괄 생성 후 저장 경로 반환. try/except로 한 장 실패 시 격리."""
    saved: list[Path] = []
    out_dir.mkdir(parents=True, exist_ok=True)
    for scene in scenes:
        try:
            scene_id = scene.get("scene_id", scenes.index(scene))
            prompt = scene["prompt_en"]
            if COMMON_STYLE:
                prompt = f"{prompt}, {COMMON_STYLE}"
            url = generate_image(prompt, model=model, seed=scene_id)
            out_path = out_dir / f"travel_{scene_id}.png"
            save_image(url, out_path, model)
            saved.append(out_path)
        except Exception as e:
            print("이미지 생성 실패: {e}")
    return saved