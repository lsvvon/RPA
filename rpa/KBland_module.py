from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import re


def KBland_streetnum(driver):
    url = "https://kbland.kr/map?xy=37.5205559,126.9265729,17"
    driver.get(url)

    # 팝업창 종료
    main = driver.window_handles

    for i in main:
        if i != main[0]:
            driver.switch_to.window(i)
            driver.close()

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # 1. input이 포함된 div 요소 기다리기
    input_div = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".homeSerchBox"))
    )
    
    # JavaScript로 클릭 시도
    driver.execute_script("arguments[0].click();", input_div)

    time.sleep(3)
    
    # input 요소가 나타날 때까지 기다린 후 주소 입력
    input_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control"))
    )
    input_element.send_keys("상봉동 495")
    input_element.send_keys(Keys.ENTER)

    time.sleep(3)

    # 면적 select 요소가 나타날 때까지 기다리고 클릭
    area_select_div = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".widthTypeValue"))
    )
    driver.execute_script("arguments[0].click();", area_select_div)

    time.sleep(3)

    # 면적 목록 요소 기다리기
    area_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tdbold"))
    )

    time.sleep(5)

    area_data = '82'  # 임의의 면적값
    cnt = 0
    area_list = []
    floor = '2' # 층
    building = 'apt' # 아파트 or 오피스텔
    for element in area_elements:
        size = element.text
        area_list.append(size)

    # 면적 리스트에서 원하는 값 찾기
    for i in range(len(area_list)):
        cnt += 1
        if area_data in area_list[i]:
            area_select = driver.find_elements(By.CLASS_NAME, "tdbold")[i]
            driver.execute_script("arguments[0].click();", area_select)
            break
    if cnt == len(area_list):
        print(f"'{area_data}' 면적을 찾을 수 없었습니다.")
        raise TimeoutException("면적 값을 찾을 수 없습니다.")  # 타임아웃 예외 발생

    time.sleep(5)

    # 숫자 추출 및 계산
    def parse_cost_value(text):
        match = re.match(r"(\d+)억\s*(\d*)", text)
        if match:
            billion = int(match.group(1)) * 10**8
            million = int(match.group(2)) * 10**4 if match.group(2) else 0
            return billion + million
        return None
    # 아파트의 최저층, 오피스텔은 하위평균가 적용
    if (floor == '1' and building == 'apt') or building=='officetel':
        # '하위평균가' 값을 가져오기
        value_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[em[text()='하위평균가']]")) 
        )
        # 텍스트 가져오기
        value_text = value_element.text  
        # '하위평균가' 제거 및 숫자만 추출
        value_text_cleaned = value_text.replace("하위평균가", "").strip()
    # 일반가 적용
    else:
        # 일반가 값 가져오기
        value_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".costvalue"))  
        )
        # 텍스트 가져오기
        value_text_cleaned = value_element.text  
    
    # 숫자로 변환
    numeric_value = parse_cost_value(value_text_cleaned)
    print(f"Parsed numeric value: {numeric_value}") 

    # 하위평균가
    low_value = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//span[em[text()='하위평균가']]")) 
    )
    # 일반가 값 
    common_value = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".costvalue"))  
    )
    low_value_text = low_value.text.replace("하위평균가", "").strip()
    common_value_text = common_value.text
    
    
    return low_value_text, common_value_text
