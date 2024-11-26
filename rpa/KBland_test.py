from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
# 자동화 메세지 옵션 제거
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)

url = "https://kbland.kr/map?xy=37.5205559,126.9265729,17"

driver.get(url)
time.sleep(1)  


# 존재하지 않는 요소 찾기
# try:
#     element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, '.nonexistent-element'))
# )
#     print(element.text)
# except NoSuchElementException as e:
#     print("요소를 찾지 못했습니다.")
# finally:
#     # 브라우저 종료
#     driver.quit()

# input이 포함되어있는 div 요소 클릭
input_div = driver.find_element(By.CLASS_NAME, "homeSerchBox")
input_div.click()
time.sleep(1)  

# input에 주소 입력 하고 엔터
input_element = driver.find_element(By.CLASS_NAME, "form-control")
input_element.send_keys("상봉동 495")
input_element.send_keys(Keys.ENTER)
time.sleep(1)  

# 면적 select 클릭
area_select_div = driver.find_element(By.CLASS_NAME, "widthTypeValue")
area_select_div.click()
time.sleep(1)   

# 면적 선택
area_list = []
area = driver.find_elements(By.CLASS_NAME, "tdbold")
area_data = '109' # 임의의 면적값

for i in area:
    size = i.text
    area_list.append(size)

for i in range(len(area_list)):
    if area_data in area_list[i]:
            area_select = driver.find_elements(By.CLASS_NAME, "tdbold")[i]
            area_select.click()
            break   
time.sleep(1)

# 화면 캡처
driver.save_screenshot('C:/시세조사/'+"kb부동산_관리번호.png")

    

