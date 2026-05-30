from pathlib import Path
import re
REQUIRED_FIELDS = ["scene_kr", "shot", "angle", "light", "composition", "lens", "prompt_en"]

def load_draft(path: Path) -> str:
    """scene_draft.md를 읽어 본문을 반환."""
    # 여기에 path.read_text(encoding='utf-8') 반환 코드를 채워요.

    return path.read_text(encoding="utf-8")
    

def count_scenes(text: str) -> int:
    """본문에서 '## 장면 N' 헤딩 수를 카운트."""
    # 여기에 re.findall + 길이 반환 코드를 채워요.

    return len(re.findall(r'^## 장면 \d+', text, re.M))

def check_fields(text: str, scene_idx: int) -> list[str]:
    """주어진 장면 인덱스에 빠진 필드 목록 반환. 모두 있으면 빈 리스트."""
    # ① ## 장면 N 섹션만 잘라냄: 다음 ## 헤딩 혹은 파일 끝까지
    section_pattern = rf'^## 장면 {scene_idx}\s*$(.*?)(?=^##|\Z)'
    match = re.search(section_pattern, text, re.M | re.S)

    missing: list[str] = []

    if not match:
        return list(REQUIRED_FIELDS)  # 섹션 자체가 없으면 전부 누락

    section = match.group(1)  # ## 장면 N 이후 ~ 다음 ## 이전 텍스트

    # ② 섹션 안에서 "- 필드명 :" 형태로 선언된 필드 이름 수집
    #    (콜론이 없는 줄은 무시됨)
    found_fields = re.findall(r'^\s*-\s*(\w+)\s*:', section, re.M)

    # ③ REQUIRED_FIELDS 중 found_fields 에 없는 것 = missing
    for field in REQUIRED_FIELDS:
        if field not in found_fields:
            missing.append(field)

    return missing

if __name__ == "__main__":
    draft = load_draft(Path("scene_draft.md"))
    print(draft)
    n = count_scenes(draft)
    print(f"[검출] 장면 수: {n}")

    # 각 장면에 대해 check_fields 호출 + 누락 출력
    all_ok = True
    for i in range(1, n + 1):
        missing = check_fields(draft, i)
        if missing:
            print(f"  장면 {i} 누락 필드: {missing}")
            all_ok = False

    if all_ok:
        print("[완료] 모든 장면 OK")