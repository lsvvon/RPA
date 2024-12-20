import etax 
import hometax
import kbland
import realtyprice
import rtech
import wetax

def main():
    print("etax 실행 중...")
    try:
        etax.main()  # etax 모듈의 main 함수 호출
        print("etax 실행 완료.")
    except Exception as e:
        print(f"etax 실행 중 오류 발생: {e}")

    # 다른 모듈도 동일한 방식으로 호출
    print("hometax 실행 중...")
    try:
        hometax.some_function()  # 실제 함수 이름으로 수정
        print("hometax 실행 완료.")
    except Exception as e:
        print(f"hometax 실행 중 오류 발생: {e}")

    print("kbland 실행 중...")
    try:
        kbland.some_function()  # 실제 함수 이름으로 수정
        print("kbland 실행 완료.")
    except Exception as e:
        print(f"kbland 실행 중 오류 발생: {e}")

    print("realtyprice 실행 중...")
    try:
        realtyprice.some_function()  # 실제 함수 이름으로 수정
        print("realtyprice 실행 완료.")
    except Exception as e:
        print(f"realtyprice 실행 중 오류 발생: {e}")

    print("rtech 실행 중...")
    try:
        rtech.some_function()  # 실제 함수 이름으로 수정
        print("rtech 실행 완료.")
    except Exception as e:
        print(f"rtech 실행 중 오류 발생: {e}")

    print("wetax 실행 중...")
    try:
        wetax.some_function()  # 실제 함수 이름으로 수정
        print("wetax 실행 완료.")
    except Exception as e:
        print(f"wetax 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
