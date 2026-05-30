import time
import statistics

from agents.image import generate_image


def time_one_call(prompt: str, seed: int, model: str = "flux") -> float:
    """이미지 1회 호출에 걸린 시간을 초 단위로 돌려주는 함수."""
    # 여기에 시작 시각을 time.perf_counter()로 기록해요
    start = time.perf_counter()

    # 여기에 generate_image(prompt=..., seed=..., model=...) 호출을 채워요
    generate_image(prompt, model, seed)

    # 여기에 종료 시각을 time.perf_counter()로 기록해요
    end = time.perf_counter()

    # 여기에 종료 시각 - 시작 시각을 반환하도록 채워요
    return end - start


def run_ab_test(prompt: str, n_calls: int = 3) -> dict:
    """같은 prompt를 seed A/B로 나누어 여러 번 호출하는 함수."""
    # 여기에 seed A=42, seed B=137 값을 준비해요 (강사 day5-s3 시연 seed 일치)
    seed_A=42
    seed_B=137

    # 여기에 A 그룹 지연 시간을 담을 리스트를 만들어요
    a_latencies = []

    # 여기에 B 그룹 지연 시간을 담을 리스트를 만들어요
    b_latencies = []

    # 여기에 n_calls만큼 A 그룹 time_one_call을 반복해요
    for _ in range(n_calls):
        a_latencies.append(time_one_call(prompt, seed_A))

    # 여기에 n_calls만큼 B 그룹 time_one_call을 반복해요
    for _ in range(n_calls):
        b_latencies.append(time_one_call(prompt, seed_B))

    # 여기에 두 리스트를 dict로 묶어 반환하도록 채워요
    return {
        "a": a_latencies,
        "b": b_latencies
    }


def compute_p95(latencies: list[float]) -> float:
    """지연 시간 목록에서 P95 값을 계산하는 함수."""
    # 여기에 빈 리스트일 때의 처리를 채워요
    # 여기에 statistics.quantiles 또는 정렬 기반 계산을 채워요
    # 여기에 초 단위 float 값을 반환하도록 채워요
    return statistics.quantiles(latencies, n=100)[94] #인덱스 94가 95번째