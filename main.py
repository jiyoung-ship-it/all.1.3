
# MAC 연산 함수
def calculate_mac(pattern, filter_data):
    score = 0.0
    size = len(pattern)

    for i in range(size):
        for j in range(size):
            score += pattern[i][j] * filter_data[i][j]

    return score


# MAC 연산 테스트
def test_mac():
    pattern = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    cross_filter = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    x_filter = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]

    cross_score = calculate_mac(pattern, cross_filter)
    x_score = calculate_mac(pattern, x_filter)

    print("\n=== MAC 연산 테스트 ===")
    print("십자가 필터 점수:", cross_score)
    print("X 필터 점수:", x_score)


# 메인 메뉴
def main():
    while True:
        print("\n=== Mini NPU 시뮬레이터 ===")
        print("1. 사용자 입력 모드 (3×3)")
        print("2. JSON 데이터 분석 모드")
        print("0. 종료")

        choice = input("모드를 선택하세요: ").strip()

        if choice == "1":
            print("사용자 입력 모드를 선택했습니다.")
            test_mac()

        elif choice == "2":
            print("JSON 데이터 분석 모드를 선택했습니다.")

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("입력 오류: 0, 1, 2 중 선택하세요.")


if __name__ == "__main__":
    main()
