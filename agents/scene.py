import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = """
    당신은 일기 텍스트를 분석하여 그림 4장면을 추출하는 어시스턴트입니다.
    출력은 반드시 JSON 객체여야 하며 다음 스키마를 따르세요:
    {
    "scenes": [
        {
        "scene_id": int,
        "scene_kr": "한국어 1줄 장면 설명",
        "prompt_en": "영문 이미지 프롬프트 1줄 (샷·앵글·조명·스타일 포함)"
        }
    ]
    }
    반드시 4개 장면을 추출하세요.
    prompt_en은 반드시 영어로 작성하고, wide shot/medium shot/close-up 중 하나, eye-level/low/high angle 중 하나, soft/rim/backlit lighting 중 하나를 포함하세요.
    # 여기에 일관성 어휘 가이드를 추가해요 (예: watercolor diary illustration 스타일 유지)
""" 


def extract_scenes(diary_text: str) -> list[dict]:
    """일기 텍스트를 받아 scenes 리스트를 반환합니다."""
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": diary_text}
        ],
        response_format= {"type": "json_object"},
        temperature= 0.7,
        max_tokens=500,
    )
    return json.loads(response.choices[0].message.content)["scenes"]


def validate_scenes(scenes: list[dict]) -> list[str]:
    """scenes 리스트가 4장면 × 필수 3필드(scene_id, scene_kr, prompt_en) 충족하는지 검증합니다."""
    REQUIRED_FIELDS = {"scene_id", "scene_kr", "prompt_en"}
    errors: list[str] = []

    if len(scenes) != 4:
        errors.append(f"scenes가 4장면이 아닙니다 (현재: {len(scenes)}장면)")

    for i, scene in enumerate(scenes):
        missing = REQUIRED_FIELDS - set(scene)
        if missing:
            errors.append(f"scene {i + 1}: {', '.join(missing)} field가 없습니다")

    return errors


def save_scenes(scenes: list[dict], out_path: str) -> None:
    """scenes 리스트를 JSON 파일로 저장합니다."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with path.open("w", encoding="utf-8") as f:
        json.dump({"scenes": scenes}, f, ensure_ascii=False, indent=2)