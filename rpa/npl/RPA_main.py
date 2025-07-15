from selenium.webdriver.chrome.options import Options
import common_module
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import CourtAuction
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
# .env 파일 활성화
load_dotenv()
AppKey = os.getenv('AppKey')
AppSecretKey = os.getenv('AppSecretKey')

# 드라이버 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


loopFlag = True

def data_insert(result, i):
    print(result)
    if i == 1:
        i = ''
    
    # 결과값 화면에 바인딩
    if result:
        response_code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Response_Code" + str(i)))
        )
        response_code_input.send_keys(result['response_code'])

        response_msg_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Response_Msg" + str(i)))
        )
        response_msg_input.send_keys(result['response_msg'].replace("’", "").strip())

        Price_High = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Price_High" + str(i)))
        )
        Price_High.send_keys(result['data'][0] if result['data'][0] is not None else '')
        
        Price_Low = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Price_Low" + str(i)))
        )
        Price_Low.send_keys(result['data'][1] if result['data'][1] is not None else '')
        
        Build_Area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Build_Area" + str(i)))
        )
        Build_Area.send_keys(result['data'][2] if result['data'][2] is not None else '')

        Base_Date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Base_Date" + str(i)))
        )
        Base_Date.send_keys(result['data'][3] if result['data'][3] is not None else '')

    else:
        print("main data insert 결과를 사용할 수 없습니다.")


def response_insert():
    Response_Code1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Response_Code1"))
    )
    Response_Msg1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Response_Msg1"))
    )
    time.sleep(1)
    # rpa 성공 여부 판단
    # if response_value:
    Response_Code1.send_keys("00000000")
    Response_Msg1.send_keys("RPA 정상적으로 처리되었습니다.")
    print("✅ RPA 실행 성공!")


# 반복 실행을 위한 while루프
# end_time = datetime.now() + timedelta(hours=4)
# now = time.localtime()  # 현재 시간 가져오기
# formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
# print(formatted_time)  # 예: 2025-02-11 14:30:45
# print(end_time)

# driver가 이미 실행 중인지 확인하고, 없으면 새로 실행
driver = None  # 초기 상태에서 driver가 없다고 가정

# while datetime.now() < end_time:
while loopFlag:

    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    start_time = now

    current_hour = 20
    # print(f"현재 시간: {current_hour}:{current_minute}")
    # 8시부터 20시까지만 try 문 실행
    if not (8 <= current_hour <= 20):        
        try:
            if driver is not None:
                driver.quit()   # driver가 None이 아니면 종료
                driver = None                
                print(f"드라이버를 종료합니다. {now}")
        except Exception as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            print(f"드라이버 종료 중 오류 발생: {error}")

        time.sleep(30)
        continue

    try:
        # 크롬 재실행 하지 않고 조회만 진행한다.
        if driver is None:
            driver = common_module.initialize_driver()
            print(f"새로운 드라이버를 시작합니다. {now}")

        url = "https://rpa.shinhanci.co.kr/Asp/ca_rpa3.htm"

        # navigator.webdriver를 false로 설정하여 자동화 도구 인식 방지
        # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "Mozilla/5.0"})
        driver.get(url)
        #print("RPA_main.driver: ", driver)
        time.sleep(2)
                
        # 조회 버튼 클릭
        try:            
            # key value
            AppKey_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "AppKey"))                
            )
            driver.execute_script("arguments[0].value = arguments[1];", AppKey_element, AppKey)

            AppSecretKey_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "AppSecretKey"))
            )
            driver.execute_script("arguments[0].value = arguments[1];", AppSecretKey_element, AppSecretKey)

            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnSearch"))
            )
            submit_button.click()
            print(f"RPA 조회 완료! {now}")

        except Exception as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            print("RPA 조회 버튼 클릭 실패:", error)
            # 드라이버 종료 후 다시 실행
            driver.quit()
            continue

        time.sleep(3)

        # 수집할 요소 정의
        elements_to_find = [
            (By.ID, "Search_Gubun1", "Search_Gubun1"),
            (By.ID, "Estate_Gubun1", "Estate_Gubun1"),
            (By.ID, "Sido1", "Sido1"),
        ]

        # 수집된 데이터 저장
        collected_data = {}

        # 요소 값 수집
        for by, value, description in elements_to_find:
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by, value))
                )
                value_attribute = element.get_attribute("value").strip() if element.get_attribute("value") else ""
                collected_data[description] = value_attribute
            except Exception as e:
                error = str(e).split(";")[0]
                error = str(error).split("\n")[0]
                print(f"{description} 요소를 찾을 수 없습니다:", error)
                collected_data[description] = "오류 발생"

        # print("collected_data", collected_data)

        # ticker와 addResch를 순서대로 매핑하여 데이터 수집
        tickers = ["Ticker", "Ticker2", "Ticker3", "Ticker4", "Ticker5", "Ticker6"]
        add_reschs = ["addResch", "addResch2", "addResch3", "addResch4", "addResch5", "addResch6"]
        ranks = ["Rank_No", "Rank_No2", "Rank_No3", "Rank_No4", "Rank_No5", "Rank_No6"]
        data = []
        dataloop = []

        for ticker_key, add_resch_key, rank_key in zip(tickers, add_reschs, ranks):
            ticker_value = collected_data.get(ticker_key)
            rank_value = collected_data.get(rank_key)
            if ticker_value and ticker_value != "":
                entry = {
                    "Ticker": ticker_value,
                    "Rank": rank_value,
                    "addResch": collected_data.get(add_resch_key, "기본값"),
                    "Search_Gubun": collected_data.get("Search_Gubun1"),
                    "Estate_Gubun": collected_data.get("Estate_Gubun1")
                }
                data.append(entry)

        # 확인용 출력
        # print(data)

        # 실행 가능한 모듈과 해당 메인 함수의 매핑
        module_mapping = {
            "Etax": lambda dataloop, kwargs: CourtAuction.main(dataloop, kwargs),
        }

        result = None
        i = 1

        # 데이터를 Ticker 순서대로 처리
        for entry in data:
            ticker = entry["Ticker"]
            addResch = entry["addResch"]
            rank = entry["Rank"]
            Search_Gubun = entry["Search_Gubun"]
            Estate_Gubun = entry["Estate_Gubun"]
            num = len(data) 

            dataloop = []
            entry2 = {
                "Ticker": ticker,
                "Rank": rank,
                "addResch": addResch,
                "Search_Gubun": Search_Gubun,
                "Estate_Gubun": Estate_Gubun
            }
            dataloop.append(entry2)
            

            ticker_start_time = now           
            print(f"{ticker} 실행 중...  {ticker_start_time}")
            
            try:
                if ticker in module_mapping:
                    result = module_mapping[ticker](
                        dataloop,
                        collected_data
                    )                    

                    # 화면값 세팅값    
                    data_insert(result, i)

                    ticker_end_time = datetime.now()                    

                    print(f"{ticker} 실행 완료. {ticker_end_time}")
                     # 경과 시간 계산 (초 단위)
                    ticker_elapsed_time = ticker_end_time - ticker_start_time
                    print(f"{ticker} 경과 시간: {ticker_elapsed_time}초")


            except Exception as e:
                error = str(e).split(";")[0]
                error = str(error).split("\n")[0]
                print(f"{ticker} 실행 중 오류 발생fdfd: {error}")
                # result['response_msg'] = f"{ticker} 실행 중 오류 발생: {e}"
                # result['response_code'] = '90000000'

            i += 1

        # 등록 버튼 클릭 : 조회값이 있으면 
        if len(data) > 0:
            try:
                # response_code, response_msg 값 넣기
                Response_Code1 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "Response_Code1"))
                )
                Response_Msg1 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "Response_Msg1"))
                )
                # key value
                AppKey_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "AppKey"))                
                )
                driver.execute_script("arguments[0].value = arguments[1];", AppKey_element, AppKey)

                AppSecretKey_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "AppSecretKey"))
                )
                driver.execute_script("arguments[0].value = arguments[1];", AppSecretKey_element, AppSecretKey)

                # rpa 성공 여부 판단
                Response_Code1.send_keys("00000000")
                Response_Msg1.send_keys("RPA 정상적으로 처리되었습니다.")
                print("✅ RPA 실행 성공!")

                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btnInsert"))
                )
                submit_button.click()

                end_time = datetime.now()
                print(f"RPA 등록 완료! {end_time}")
                # time.sleep(3)

                # 경과 시간 계산 (초 단위)
                elapsed_time = end_time - start_time
                print(f"경과 시간: {elapsed_time}초")

            except Exception as e:
                error = str(e).split(";")[0]
                error = str(error).split("\n")[0]
                print("RPA 등록 버튼 클릭 실패:", error)
                # time.sleep(3)    

        # 드라이버 종료 후 다시 실행
        #driver.quit()
        time.sleep(3)

        # loopFlag = False

    except Exception as e:
        error = str(e).split(";")[0]
        error = str(error).split("\n")[0]
        print("오류 발생:", error)
        driver.quit()
        time.sleep(3)

