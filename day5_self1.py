import json
from pathlib import Path

from ab_test import compute_p95, run_ab_test


BASE_DIR = Path(__file__).parent
DOMAIN_NAME = "travel"
N_CALLS = 3


def main() -> None:
    # Step 1. 도메인 프롬프트 JSON 로드
    domain_path = BASE_DIR / "domains" / f"{DOMAIN_NAME}_prompts.json"
    # 여기에 domain_path에서 JSON을 읽는 코드를 채워요
    data = json.loads(Path(domain_path).read_text(encoding="utf-8"))

    # 여기에 scenes 목록에서 사용할 장면 1개를 고르는 코드를 채워요
    print(data['scenes'][0])
    scene = data['scenes'][0]

    # 여기에 diary_sentence와 prompt_addons를 합쳐 prompt를 만드는 코드를 채워요
    prompt = scene['diary_sentence'] + ', ' + ', '.join(scene['prompt_addons'])
    print(prompt)

    # Step 2. A/B 실행 + P95 계산
    # 여기에 run_ab_test(prompt, n_calls=N_CALLS)를 호출해요
    ab_result = run_ab_test(prompt, N_CALLS)

    # 여기에 A 그룹 지연 목록을 꺼내요
    # 여기에 B 그룹 지연 목록을 꺼내요
    # 여기에 compute_p95로 p95_a와 p95_b를 계산해요
    p95_a = compute_p95(ab_result['a'])
    p95_b = compute_p95(ab_result['b'])

    # Step 3. ab_test_results.json 저장
    result_path = BASE_DIR / "ab_test_results.json"
    # 여기에 domain, seed, latencies, p95 값을 dict로 묶어요
    domain_data = {
        "domain": DOMAIN_NAME,
        "seed_a": 42,
        "seed_b": 137,
        "latencies": {"a": ab_result['a'], "b": ab_result['b']},
        "p95": {"a": p95_a, "b": p95_b},
    }
    result_path.write_text(json.dumps(domain_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Step 4. cost_report.md 작성
    report_path = BASE_DIR / "cost_report.md"

    # 5일 누적 비용 표
    cost_table = (
        "## 5일 누적 비용\n\n"
        "| Day | 주요 작업 | 호출 수 | 단가 또는 추정 단가 | 합계 |\n"
        "|---|---|---:|---:|---:|\n"
        "| Day 1 | 환경 확인과 첫 호출 | 2 | $0.10 | $0.20 |\n"
        "| Day 2 | 장면 JSON 생성 | 4 | $0.13 | $0.50 |\n"
        "| Day 3 | 이미지 생성 | 4 | $0.20 | $0.80 |\n"
        "| Day 4 | 영상 생성 | 2 | $0.50 | $1.00 |\n"
        f"| Day 5 | 도메인 A/B 테스트 ({DOMAIN_NAME}) | {N_CALLS * 2} | $0.08 | $0.50 |\n"
        "| 합계 |  | 18 |  | $3.00 |\n"
    )

    # P95 지연 섹션
    p95_section = (
        "## P95 지연\n\n"
        "| 그룹 | seed | 호출 수 | P95 지연 |\n"
        "|---|---:|---:|---:|\n"
        f"| A | 42 | {N_CALLS} | {p95_a:.2f}초 |\n"
        f"| B | 137 | {N_CALLS} | {p95_b:.2f}초 |\n"
    )

    report_path.write_text(
        f"# 그림일기 파이프라인 5일 누적 비용 보고서\n\n{cost_table}\n{p95_section}",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()