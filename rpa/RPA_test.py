import Etax_module
import common_module
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support.select import Select
import ssl



driver = common_module.initialize_driver()
url = "https://bizssl.shinhanci.co.kr/SHSCHER/Asp/RPA/CA_RPA_Condition.asp"
driver.get(url)

time.sleep(5)


# 요소 검색 및 출력
elements_to_find = [
    (By.ID, "Search_Gubun1", "Search_Gobun1"),
    (By.ID, "Estate_Gubun1", "Estate_Gubun1"),
    (By.ID, "Sigungu1", "Sigungu1"),
    (By.ID, "Ridong1", "Ridong1"),
    (By.ID, "Jibun_No1", "Jibun_No1"),
    (By.ID, "Jibun_No2", "Jibun_No2"),
    (By.ID, "Building_Name1", "Building_Name1"),
    (By.ID, "Building_No1", "Building_No1"),
    (By.ID, "Building_No2", "Building_No2"),
    (By.ID, "Room_No1", "Room_No1"),
    (By.ID, "Doro_Name1", "Doro_Name1"),
    (By.ID, "Chosung1", "Chosung1"),
    (By.ID, "Ticker", "Ticker"),
    (By.ID, "Ticker2", "Ticker2"),
    (By.ID, "Ticker3", "Ticker3"),
    (By.ID, "Ticker4", "Ticker4"),
    (By.ID, "Ticker5", "Ticker5"),
    (By.ID, "addResch", "addResch"),
    (By.ID, "addResch2", "addResch2"),
    (By.ID, "addResch3", "addResch3"),
    (By.ID, "addResch4", "addResch4"),
    (By.ID, "addResch5", "addResch5"),
]

for by, value, description in elements_to_find:
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((by, value))
        )
        # 텍스트와 value 속성을 모두 출력
        value_attribute = element.get_attribute("value")
        print(f"{description} - Value: {value_attribute}")
    except Exception as e:
        print(f"{description} 요소를 찾을 수 없습니다:", e)


# 드라이버 종료
driver.quit()