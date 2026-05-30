# day1_self1.py — 그림일기 첫 장면 DALL-E 호출
import os, requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import base64


def load_api_key() -> str:
    """`.env`에서 OPENAI_API_KEY를 로드하고 마스킹한 키 첫 5자를 출력합니다."""
    load_dotenv()
    apiKey: str | None = os.getenv("OPENAI_API_KEY")
    return apiKey[:5]


def build_scene_prompt() -> str:
    """본인 일기 첫 문장을 영문으로 묘사한 프롬프트를 반환합니다."""
    # 여기에 일기 첫 장면을 영문 묘사로 작성해요.
    # 여기에 본인 프롬프트 문장을 채워요.

    return "business district, office workers, skyscrapers, urban walk, city energy, aspiration, motivation, belonging, corporate life, metropolitan, inspiration, future career, positive energy, downtown, professionals, rainy breeze, reflective mood, hopeful atmosphere"

def generate_image(client: OpenAI, prompt: str) -> str:
    """DALL-E 3로 이미지 1장 생성, URL을 반환합니다."""
    # 여기에 client.images.generate(...)를 호출하고 response.data[0].url을 반환하는 코드를 채워요.

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        n=1
    )
    return response.data[0].b64_json

def save_image(image_base64: str, out_path: Path) -> None:
    """URL의 PNG 바이트를 내려받아 out_path에 저장합니다."""
    # 여기에 requests.get(url).content로 바이트 다운로드 + out_path.write_bytes(...) 코드를 채워요.
    image_bytes = base64.b64decode(image_base64)

    out_path.write_bytes(image_bytes)


if __name__ == "__main__":
    load_api_key()
    client = OpenAI()

    prompt = build_scene_prompt()
    print(f"[프롬프트] {prompt}")

    base64Image = generate_image(client, prompt)
    print(f"[응답 URL] {base64Image[:60]}...")

    out_path = Path("outputs") / "scene01_dalle.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(base64Image, out_path)
    print(f"[저장 완료] {out_path}")