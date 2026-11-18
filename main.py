
def main():
    while True:
        print("\n=== Mini NPU 시뮬레이터 ===")
        print("1. 사용자 입력 모드 (3×3)")
        print("2. JSON 데이터 분석 모드")
        print("0. 종료")

        choice = input("모드를 선택하세요: ").strip()

        if choice == "1":
            print("사용자 입력 모드를 선택했습니다.")

        elif choice == "2":
            print("JSON 데이터 분석 모드를 선택했습니다.")

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("입력 오류: 0, 1, 2 중 선택하세요.")


if __name__ == "__main__":
    main()
