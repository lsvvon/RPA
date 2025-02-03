from selenium.webdriver.chrome.options import Options
import common_module
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import Etax
import Hometax
import KBland
import Realty1
import Realty2
import Realty3
import Rtech1
import Rtech2
import Wetax
import os

# 드라이버 초기화
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = common_module.initialize_driver()
url = "https://bizssl.shinhanci.co.kr/SHSCHER/Asp/RPA/CA_RPA_Condition.asp"
driver.get(url)
#print("RPA_main.driver: ", driver)
time.sleep(5)

# 수집할 요소 정의
elements_to_find = [
    (By.ID, "Search_Gubun1", "Search_Gubun1"),
    (By.ID, "Estate_Gubun1", "Estate_Gubun1"),
    (By.ID, "Sido1", "Sido1"),
    (By.ID, "Sigungu1", "Sigungu1"),
    (By.ID, "Sigungu2", "Sigungu2"),
    (By.ID, "Ridong1", "Ridong1"),
    (By.ID, "Jibun_No1", "Jibun_No1"),
    (By.ID, "Jibun_No2", "Jibun_No2"),
    (By.ID, "Building_Name1", "Building_Name1"),
    (By.ID, "Building_No1", "Building_No1"),
    (By.ID, "Building_No2", "Building_No2"),
    (By.ID, "Room_No1", "Room_No1"),
    (By.ID, "Doro_Name1", "Doro_Name1"),
    (By.ID, "Chosung1", "Chosung1"),
    (By.ID, "Build_Area1", "Build_Area1"),
    (By.ID, "Lease_Inv_Mng_No1", "Lease_Inv_Mng_No1"),
    (By.ID, "Floor1", "Floor1"),
    (By.ID, "Ticker", "Ticker"),
    (By.ID, "Ticker2", "Ticker2"),
    (By.ID, "Ticker3", "Ticker3"),
    (By.ID, "Ticker4", "Ticker4"),
    (By.ID, "Ticker5", "Ticker5"),
    (By.ID, "Ticker6", "Ticker6"),
    (By.ID, "addResch", "addResch"),
    (By.ID, "addResch2", "addResch2"),
    (By.ID, "addResch3", "addResch3"),
    (By.ID, "addResch4", "addResch4"),
    (By.ID, "addResch5", "addResch5"),
    (By.ID, "addResch6", "addResch6"),
    (By.ID, "Rank_No", "Rank_No"),
    (By.ID, "Rank_No2", "Rank_No2"),
    (By.ID, "Rank_No3", "Rank_No3"),
    (By.ID, "Rank_No4", "Rank_No4"),
    (By.ID, "Rank_No5", "Rank_No5"),
    (By.ID, "Rank_No6", "Rank_No6"),

]

# 수집된 데이터 저장
collected_data = {}

# 요소 값 수집
for by, value, description in elements_to_find:
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((by, value))
        )
        value_attribute = element.get_attribute("value").strip() if element.get_attribute("value") else ""
        collected_data[description] = value_attribute
    except Exception as e:
        print(f"{description} 요소를 찾을 수 없습니다:", e)
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
    "Etax": lambda dataloop, kwargs: Etax.main(dataloop, kwargs),
    "Wetax": lambda dataloop, kwargs: Wetax.main(dataloop, kwargs),
    "Hometax": lambda dataloop, kwargs: Hometax.main(dataloop, kwargs),
    "KBLand": lambda dataloop, kwargs: KBland.main(dataloop, kwargs),
    "Realty1": lambda dataloop, kwargs: Realty1.main(dataloop, kwargs),
    "Realty2": lambda dataloop, kwargs: Realty2.main(dataloop, kwargs),
    "Realty3": lambda dataloop, kwargs: Realty3.main(dataloop, kwargs),
    "Rtech": lambda dataloop, kwargs: Rtech1.main(dataloop, kwargs),
    "Rtech2": lambda dataloop, kwargs: Rtech2.main(dataloop, kwargs),  
}

def data_insert(result, i):
    
    if i == 1:
        i = ''

    if result:
        response_code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Response_Code" + str(i)))
        )
        response_code_input.send_keys(result['response_code'])

        response_msg_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Response_Msg" + str(i)))
        )
        response_msg_input.send_keys(result['response_msg'])

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

# 첨부 파일 처리
def file_attach(dataloop, collected_data, i):    
    # file_name = "5000000000_901.png"  # 업로드하려는 파일 이름
    folder_path = r"C:\python\RPA\rpa\capImg"  # capImg 폴더의 절대 경로
    # file_path = os.path.join(folder_path, file_name)

    Lease_Inv_Mng_No = collected_data.get('Lease_Inv_Mng_No1')
       
    for entry in dataloop:
        Rank = entry.get("Rank") 

    # 파일 경로 설정
    next_seq = "70" + Rank
    file_name = f"{Lease_Inv_Mng_No}_{next_seq}.png"    
    file_path = os.path.join(folder_path, file_name)

    if i == 1:
        i = ''
    
    print("file_path:", file_path, i)

    # 파일 첨부
    txtFile_capImg = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "txtFile" + str(i)))
    )
    txtFile_capImg.send_keys(file_path)
 

def main(data):
    result = None
    i = 1
    KBland_ResCode = ''
    Rtech_ResCode = ''
    Etc_ResCode = ''

    # 데이터를 Ticker 순서대로 처리
    for entry in data:
        ticker = entry["Ticker"]
        addResch = entry["addResch"]
        rank = entry["Rank"]
        Search_Gubun = entry["Search_Gubun"]
        Estate_Gubun = entry["Estate_Gubun"]

        dataloop = []
        entry2 = {
            "Ticker": ticker,
            "Rank": rank,
            "addResch": addResch,
            "Search_Gubun": Search_Gubun,
            "Estate_Gubun": Estate_Gubun
        }
        dataloop.append(entry2)

        print(f"{ticker} 실행 중...")

        # 우선순위 정상처리되면 종료한다.
        if KBland_ResCode == '00000000' and Rtech_ResCode == '00000000':
            break
        if Etc_ResCode == '00000000':     
            break
        
        try:
            if ticker in module_mapping:
                if ticker == "Rtech2":
                    result = module_mapping[ticker](
                    dataloop,
                    collected_data
                )                    

                # if ticker == 'KBLand':
                #     KBland_ResCode = result['response_code']
                # elif ticker == 'Rtech':
                #     Rtech_ResCode = result['response_code']
                # else: 
                #     Etc_ResCode = result['response_code']

                # print(f"{ticker} : response value!!!")    
                # print("KBland_ResCode:", KBland_ResCode)
                # print("Rtech_ResCode:", Rtech_ResCode)
                # print("Etc_ResCode:", Etc_ResCode)

                # 화면값 세팅값    
                data_insert(result, i)
                # 첨부 파일 처리
                file_attach(dataloop, collected_data, i)

                print(f"{ticker} 실행 완료.")
                
            else:
                print(f"{ticker} 실행 중 오류 발생")
                # result['response_msg'] = f"{ticker} 실행 중 오류 발생: {e}"
                # result['response_code'] = '90000000'
        except Exception as e:
            print(f"{ticker} 실행 중 오류 발생fdfd: {e}")
            # result['response_msg'] = f"{ticker} 실행 중 오류 발생: {e}"
            # result['response_code'] = '90000000'

        i += 1

if __name__ == "__main__":
    main(data)
    