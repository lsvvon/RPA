from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime

# 최대 시도 횟수 설정
MAX_RETRIES = 3
attempt = 0

while attempt < MAX_RETRIES:
    try:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        driver = webdriver.Chrome(options=options)
        url = "https://kbland.kr/map?xy=37.5205559,126.9265729,17"
        driver.get(url)

        # 페이지 로드가 완료될 때까지 기다리기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("페이지가 로드되었습니다.")

        # 1. input이 포함된 div 요소 기다리기
        print("1. input이 포함된 div 요소 기다리기")
        input_div = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".homeSerchBox"))
        )
        
        # JavaScript로 클릭 시도
        driver.execute_script("arguments[0].click();", input_div)
        
        # input 요소가 나타날 때까지 기다린 후 주소 입력
        print("2. input 요소가 나타날 때까지 기다린 후 주소 입력")
        input_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control"))
        )
        input_element.send_keys("상봉동 495")
        input_element.send_keys(Keys.ENTER)

        # 면적 select 요소가 나타날 때까지 기다리고 클릭
        print("3. 면적 select 요소가 나타날 때까지 기다리고 클릭")
        area_select_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".widthTypeValue"))
        )
        driver.execute_script("arguments[0].click();", area_select_div)

        # 면적 목록 요소 기다리기
        print("4. 면적 목록 요소 기다리기")
        area_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tdbold"))
        )

        area_data = '109'  # 임의의 면적값
        cnt = 0
        area_list = []
        for element in area_elements:
            size = element.text
            area_list.append(size)

        # 면적 리스트에서 원하는 값 찾기
        print("5. 면적 값 찾기 및 클릭")
        for i in range(len(area_list)):
            cnt += 1
            if area_data in area_list[i]:
                area_select = driver.find_elements(By.CLASS_NAME, "tdbold")[i]
                driver.execute_script("arguments[0].click();", area_select)
                break
        if cnt == len(area_list):
            print(f"'{area_data}' 면적을 찾을 수 없었습니다.")
            raise TimeoutException("면적 값을 찾을 수 없습니다.")  # 타임아웃 예외 발생


        # 화면 캡처 전 몇 초간 기다리기 (화면 로딩 완료 대기)
        time.sleep(3)

        # 현재 시간 기반으로 파일명 변경
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'C:/시세조사/kb부동산_관리번호_{timestamp}.png'

        # 화면 캡처
        driver.save_screenshot(screenshot_path)
        print(f"캡처 완료: {screenshot_path}")
                
        # 캡처 완료 후 루프를 탈출하도록 시도 횟수를 최대값으로 설정
        attempt = MAX_RETRIES

    except TimeoutException as e:
        print(f"타임아웃 발생: {e}, 재시도 중...")
        attempt += 1
        driver.quit()  # 타임아웃 발생 시 드라이버 종료 후 새로 시도

    finally:
        if attempt >= MAX_RETRIES:
            print("최대 시도 횟수 초과, 프로그램 종료.")
            driver.quit()
