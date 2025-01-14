import KBland_module
import common_module
from selenium.common.exceptions import TimeoutException


MAX_RETRIES = 3


def main(Search_Gobun, **kwargs):
    attempt = 0
    driver = None
    response_code = ""
    response_msg = ""
    realty_value = None  # realty_value 초기화

    try:
        while attempt < MAX_RETRIES:
            driver = common_module.initialize_driver()
            try:
                if Search_Gobun == '1': # 지번검색일때
                    realty_value = KBland_module.KBland_streetnum(driver, **kwargs)
                    common_module.screenshot_save(driver, "KBland_capImg")
                    response_code = '00000000'
                    response_msg = "프로그램이 정상적으로 실행되었습니다."
                    break
                elif Search_Gobun == '2':   # 도로명검색일때
                    realty_value = KBland_module.KBland_roadnum(driver, **kwargs)
                    common_module.screenshot_save(driver, "KBland_capImg")
                    response_code = '00000000'
                    response_msg = "프로그램이 정상적으로 실행되었습니다."
                    break  # 성공하면 반복 종료
            except TimeoutException as e:
                response_code = '90000000'
                response_msg = f"타임아웃 발생: {e}, 재시도 중..."
                attempt += 1
                driver.quit()  # 타임아웃 발생 시 드라이버 종료 후 새로 시도
        else:
            # MAX_RETRIES에 도달한 경우
            response_code = '90000000'
            response_msg = "최대 재시도 횟수에 도달했습니다. 프로그램 종료."

        data = {
            "realty_value": realty_value,
            "response_code": response_code,  # 응답 코드
            "response_msg": response_msg,    # 응답 메시지
        }

        return data
    
    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    Search_Gobun = '1'
    main(Search_Gobun)