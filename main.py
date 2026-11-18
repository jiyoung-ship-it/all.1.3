
from time import perf_counter_ns


# MAC 연산 함수
def calculate_mac(pattern, filter_data):
    score = 0.0
    size = len(pattern)

    for i in range(size):
        for j in range(size):
            score += pattern[i][j] * filter_data[i][j]

    return score


# MAC 점수 비교 및 판정 함수
def decide_result(score_a, score_b):
    epsilon = 1e-9

    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"

    elif score_a > score_b:
        return "A"

    else:
        return "B"


# 3×3 배열 입력 함수
def input_matrix(name):
    matrix = []

    print(f"\n{name}를 입력하세요. (3×3)")

    for i in range(3):
        while True:
            values = input(f"{i + 1}행: ").split()

            if len(values) != 3:
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
                continue

            try:
                row = [float(value) for value in values]
                matrix.append(row)
                break

            except ValueError:
                print("입력 오류: 숫자만 입력하세요.")

    return matrix


# 배열 출력 함수
def show_matrix(name, matrix):
    print(f"\n{name}")
    for row in matrix:
        print(*row)


# MAC 연산 시간 측정 함수
def timed_mac(pattern, filter_data):
    start = perf_counter_ns()
    score = calculate_mac(pattern, filter_data)
    end = perf_counter_ns()

    elapsed_ms = (end - start) / 1_000_000
    return score, elapsed_ms


# 평균 MAC 연산 시간 측정 함수
def average_mac_time(pattern, filter_data):
    repeat = 10
    total_ns = 0

    for _ in range(repeat):
        start = perf_counter_ns()
        calculate_mac(pattern, filter_data)
        end = perf_counter_ns()

        total_ns += end - start

    return total_ns / repeat / 1_000_000


# 사용자 입력 모드
def manual_mode():
    print("\n=== 사용자 입력 모드 (3×3) ===")

    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")

    print("\n=== 필터 저장 확인 ===")
    show_matrix("필터 A", filter_a)
    show_matrix("필터 B", filter_b)

    pattern = input_matrix("패턴")

    score_a, time_a = timed_mac(pattern, filter_a)
    score_b, time_b = timed_mac(pattern, filter_b)

    result = decide_result(score_a, score_b)

    print("\n=== MAC 연산 결과 ===")
    print(f"필터 A 점수: {score_a}")
    print(f"필터 B 점수: {score_b}")
    print(f"필터 A 연산 시간: {time_a:.6f} ms")
    print(f"필터 B 연산 시간: {time_b:.6f} ms")
    print(f"판정 결과: {result}")

    print("\n=== 3×3 성능 분석 ===")
    avg_a = average_mac_time(pattern, filter_a)
    avg_b = average_mac_time(pattern, filter_b)

    print("반복 측정: 10회")
    print("연산 횟수: 9회 (3×3)")
    print(f"필터 A 평균 시간: {avg_a:.6f} ms")
    print(f"필터 B 평균 시간: {avg_b:.6f} ms")


# 메인 메뉴
def main():
    while True:
        print("\n=== Mini NPU 시뮬레이터 ===")
        print("1. 사용자 입력 모드 (3×3)")
        print("2. JSON 데이터 분석 모드")
        print("0. 종료")

        choice = input("모드를 선택하세요: ").strip()

        if choice == "1":
            manual_mode()

        elif choice == "2":
            print("JSON 데이터 분석 모드를 선택했습니다.")

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("입력 오류: 0, 1, 2 중 선택하세요.")


if __name__ == "__main__":
    main()
