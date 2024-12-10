from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import full_screenshot
import os


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
    
    # input 요소가 나타날 때까지 기다린 후 주소 입력
    input_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control"))
    )
    input_element.send_keys("상봉동 495")
    input_element.send_keys(Keys.ENTER)

    # 면적 select 요소가 나타날 때까지 기다리고 클릭
    area_select_div = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".widthTypeValue"))
    )
    driver.execute_script("arguments[0].click();", area_select_div)

    # 면적 목록 요소 기다리기
    area_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tdbold"))
    )

    area_data = '109'  # 임의의 면적값
    cnt = 0
    area_list = []
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

    # 화면 캡처 전 몇 초간 기다리기 (화면 로딩 완료 대기)
    time.sleep(3)