import realtyprice_module
from selenium.common.exceptions import TimeoutException
import common_module
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import RPA_main

MAX_RETRIES = 1

def send_to_url(driver, data):
    try:
        print(data)
        # WebDriverWait을 사용하여 입력 필드가 준비될 때까지 기다림
        response_code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Response_Code"))
        )
        response_code_input.send_keys(data['response_code'])
        
        response_msg_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Response_Msg"))
        )
        response_msg_input.send_keys(data['response_msg'])

        realty_price_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Price_High"))
        )
        realty_price_input.send_keys(data['realty_price'])

        print("데이터 입력 완료")

    except Exception as e:
        print(f"데이터 입력 중 오류 발생: {e}")

def main(Search_Gubun, **kwargs):
    attempt = 0
    driver = None 
    response_code = ""
    response_msg = ""
    realty_value = None  # realty_value 초기화

    try:
        while attempt < MAX_RETRIES:
            driver = common_module.initialize_driver()

            try:
                if Search_Gubun == '1':
                    realty_value = realtyprice_module.realtyprice_apt_streetnum(driver, **kwargs)
                    common_module.screenshot_save(driver)
                    response_code = '00000000'
                    break  
                elif Search_Gubun == '2':
                    realty_value = realtyprice_module.realtyprice_apt_roadnum(driver, **kwargs)
                    common_module.screenshot_save(driver)
                    response_code = '00000000'
                    break                  
            except TimeoutException as e:
                response_code = '90000000'
                response_msg = f"타임아웃 발생: {e}, 재시도 중..."
                attempt += 1
                driver.quit()  # 타임아웃 발생 시 드라이버 종료 후 새로 시도
        else:
            # MAX_RETRIES에 도달한 경우
            response_code = '90000000'
            response_msg = "최대 재시도 횟수에 도달했습니다. 프로그램 종료."

        # driver = common_module.initialize_driver()

        # # URL로 이동
        # target_url = "https://bizssl.shinhanci.co.kr/SHSCHER/Asp/RPA/CA_RPA_Condition.asp"
        # driver.get(target_url)  # 지정된 URL로 이동

        # # 페이지가 로드될 때까지 기다림 (10초 대기)
        # WebDriverWait(driver, 10).until(
        #     EC.url_to_be(target_url)
        # )
        # # 현재 URL 확인
        # current_url = driver.current_url
        # print(f"현재 URL: {current_url}")  # 현재 URL 출력

    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")


    # 리턴값을 URL의 데이터로 매핑하여 전송
    data = {
        "realty_price": realty_value, # 개별주택가격 or 공동주택가격
        "response_code": response_code,  # 응답 코드
        "response_msg": response_msg,    # 응답 메시지
    }

    print(realty_value, response_code, response_msg)
    #send_to_url(RPA_main.driver, data)  # URL에 데이터 전송
    #print("RPA_main.driver: ", RPA_main.driver)

if __name__ == "__main__":
    main()