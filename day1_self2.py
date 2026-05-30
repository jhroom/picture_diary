import os, requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from day1_self1 import build_scene_prompt
import base64


def build_prompt_variants() -> list[tuple[str, str]]:
    """(filename, prompt) 튜플 3개를 반환합니다. WS / CU / low angle 변형 순서."""
    # 여기에 §3에서 채운 표를 기반으로 (filename, prompt_en) 3개 튜플을 채워요.
    # 힌트: filename은 outputs/scene01_ws.png · _cu.png · _low.png.
    # 힌트: prompt_en은 §2 시각 어휘 3종 표에서 골라 1줄 영문.
    base_prompt = build_scene_prompt() + "맑고 밝은 하늘 과 나무들"
    variants: list[tuple[str, str]] = [
        ("scene01_ws.png",  f"wide shot, {base_prompt}"),
        ("scene01_cu.png",  f"close up, {base_prompt}"),
        ("scene01_low.png", f"low angle shot, {base_prompt}"),
    ]

    return variants

def call_dalle(client: OpenAI, prompt: str) -> str:
    """DALL-E 3로 이미지 1장 생성, URL을 반환합니다."""
    # 여기에 client.images.generate(...)를 호출하고 response.data[0].url을 반환하는 코드를 채워요.
    # 힌트: model="dall-e-3", size="1024x1024", quality="standard", n=1.
    return client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="medium",
        n=1
    ).data[0].b64_json
    

def save_image(url: str, out_path: Path) -> None:
    """URL의 PNG 바이트를 내려받아 out_path에 저장합니다."""
    # 여기에 requests.get + write_bytes 코드를 채워요. (day1_self1.py에서 작성한 패턴 재사용)
    image_bytes = base64.b64decode(url)

    out_path.write_bytes(image_bytes)

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI()
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    variants = build_prompt_variants()
    for filename, prompt in variants:
        print(f"[호출 시작] {filename} ...")
        # 여기에 try/except로 한 장 실패해도 나머지가 진행되도록 안전 호출 + 저장 코드를 채워요.
        # 힌트: try: url = call_dalle(client, prompt) → save_image(url, output_dir / filename) → print(저장 완료)
        #       except Exception as e: print(f"[실패] {filename}: {e}") → continue
        try:
            b64 = call_dalle(client, prompt)
            save_image(b64, output_dir / filename)
            print(f"[저장 완료] {filename}")
        except Exception as e:
            print(f"[실패] {filename}: {e}")
            continue
    print("\n끝. outputs/ 폴더에서 3장을 비교해 보세요.")