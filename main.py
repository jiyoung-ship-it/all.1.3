
import json
import re
from pathlib import Path
from time import perf_counter_ns


# MAC 연산 함수
def calculate_mac(pattern, filter_data):
    score = 0.0
    size = len(pattern)

    for i in range(size):
        for j in range(size):
            score += pattern[i][j] * filter_data[i][j]

    return score


# MAC 점수 비교 및 판정
def decide_result(score_a, score_b, label_a="A", label_b="B"):
    epsilon = 1e-9

    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"
    elif score_a > score_b:
        return label_a
    else:
        return label_b


# 3×3 배열 입력
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


# 배열 출력
def show_matrix(name, matrix):
    print(f"\n{name}")
    for row in matrix:
        print(*row)


# MAC 연산 시간 측정
def timed_mac(pattern, filter_data):
    start = perf_counter_ns()
    score = calculate_mac(pattern, filter_data)
    end = perf_counter_ns()

    return score, (end - start) / 1_000_000


# 평균 MAC 연산 시간 측정
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

    performance_analysis(pattern_3=pattern, filter_3=filter_a)


# 라벨 정규화
def normalize_label(label):
    if not isinstance(label, str):
        return None

    label = label.strip().lower()

    if label in ("+", "cross"):
        return "Cross"
    if label == "x":
        return "X"

    return None


# 배열 크기 및 숫자 검증
def validate_matrix(matrix, size, name):
    if not isinstance(matrix, list) or len(matrix) != size:
        raise ValueError(f"{name}: 행 수가 {size}개가 아닙니다.")

    for i, row in enumerate(matrix, start=1):
        if not isinstance(row, list) or len(row) != size:
            raise ValueError(f"{name}: {i}행의 열 수가 {size}개가 아닙니다.")

        if any(
            isinstance(value, bool) or not isinstance(value, (int, float))
            for value in row
        ):
            raise ValueError(f"{name}: {i}행에 숫자가 아닌 값이 있습니다.")


# 크기별 MAC 성능 분석
def performance_analysis(data=None, pattern_3=None, filter_3=None):
    cross_3 = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    samples = {
        3: (
            pattern_3 if pattern_3 is not None else cross_3,
            filter_3 if filter_3 is not None else cross_3
        )
    }

    if data is not None:
        for size in (5, 13, 25):
            try:
                pattern = data["patterns"][f"size_{size}_1"]["input"]
                filter_data = data["filters"][f"size_{size}"]["cross"]

                validate_matrix(pattern, size, "패턴")
                validate_matrix(filter_data, size, "Cross 필터")

                samples[size] = (pattern, filter_data)

            except (KeyError, ValueError, TypeError) as error:
                print(f"{size}×{size} 성능 분석 제외: {error}")

    print("\n=== 크기별 MAC 성능 분석 ===")
    print("반복 측정: 각 크기별 10회")
    print(f"{'크기':<10} {'평균 시간(ms)':>16} {'연산 횟수(N²)':>16}")

    for size, (pattern, filter_data) in samples.items():
        avg_time = average_mac_time(pattern, filter_data)
        size_text = f"{size}×{size}"

        print(f"{size_text:<10} {avg_time:>16.6f} {size * size:>16}")


# JSON 분석 모드
def json_mode():
    print("\n=== JSON 데이터 분석 모드 ===")

    file_path = Path(__file__).with_name("data.json")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"JSON 파일 로드 실패: {error}")
        return

    if not isinstance(data, dict):
        print("JSON 스키마 오류: 최상위 구조는 객체여야 합니다.")
        return

    filters = data.get("filters")
    patterns = data.get("patterns")

    if not isinstance(filters, dict) or not isinstance(patterns, dict):
        print("JSON 스키마 오류: filters와 patterns는 객체여야 합니다.")
        return

    # 7단계: 테스트 집계 변수
    total_tests = len(patterns)
    passed_tests = 0
    failed_cases = []

    for case_id, item in patterns.items():
        print(f"\n[{case_id}]")

        try:
            match = re.fullmatch(r"size_(\d+)_(\d+)", case_id)

            if not match:
                raise ValueError("케이스 키 형식 오류 (예: size_5_1)")

            size = int(match.group(1))

            if not isinstance(item, dict):
                raise ValueError("패턴 데이터가 객체가 아닙니다.")

            pattern = item.get("input")
            expected = normalize_label(item.get("expected"))

            if expected is None:
                raise ValueError("expected 라벨이 올바르지 않습니다.")

            validate_matrix(pattern, size, "패턴")

            filter_group = filters.get(f"size_{size}")

            if not isinstance(filter_group, dict):
                raise ValueError(f"size_{size} 필터가 없습니다.")

            normalized_filters = {}

            for key, matrix in filter_group.items():
                label = normalize_label(key)

                if label is None or label in normalized_filters:
                    raise ValueError(f"필터 키 오류 또는 중복: {key}")

                validate_matrix(matrix, size, f"{label} 필터")
                normalized_filters[label] = matrix

            if "Cross" not in normalized_filters or "X" not in normalized_filters:
                raise ValueError("Cross/X 필터가 모두 필요합니다.")

            score_cross, time_cross = timed_mac(
                pattern, normalized_filters["Cross"]
            )

            score_x, time_x = timed_mac(
                pattern, normalized_filters["X"]
            )

            result = decide_result(score_cross, score_x, "Cross", "X")
            status = "PASS" if result == expected else "FAIL"

            print(f"Cross 점수: {score_cross:.6f} ({time_cross:.6f} ms)")
            print(f"X 점수: {score_x:.6f} ({time_x:.6f} ms)")
            print(f"판정: {result} / expected: {expected} → {status}")

            if status == "PASS":
                passed_tests += 1
            else:
                reason = f"예상 {expected}, 실제 {result}"
                failed_cases.append((case_id, reason))
                print(f"실패 사유: {reason}")

        except (ValueError, TypeError, KeyError) as error:
            reason = str(error)
            failed_cases.append((case_id, reason))
            print(f"FAIL - 실패 사유: {reason}")

    performance_analysis(data=data)

    # 7단계: 전체 결과 요약
    print("\n=== 전체 테스트 결과 요약 ===")
    print(f"전체 테스트 수: {total_tests}")
    print(f"통과 수(PASS): {passed_tests}")
    print(f"실패 수(FAIL): {len(failed_cases)}")

    if failed_cases:
        print("\n실패 케이스 목록:")
        for case_id, reason in failed_cases:
            print(f"- {case_id}: {reason}")
    else:
        print("모든 테스트를 통과했습니다.")


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
            json_mode()

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("입력 오류: 0, 1, 2 중 선택하세요.")


if __name__ == "__main__":
    main()
