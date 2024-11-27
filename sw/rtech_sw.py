import ssl
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from PIL import Image
import os

# SSL 인증서 검증 무시 설정
# ssl._create_default_https_context = ssl._create_unverified_context

# 최대 시도 횟수 설정
MAX_RETRIES = 3
attempt = 0

# # 캡차 이미지 저장 경로 설정
# save_path = r"C:\시세조사\캡챠"
# if not os.path.exists(save_path):
#     os.makedirs(save_path)

while attempt < MAX_RETRIES:
    try:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)
        # 자동화 메세지 옵션 제거
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        driver = webdriver.Chrome(options=options)

        url = "https://rtech.or.kr/main/mapSearch.do?posX="
        driver.get(url)

        # 1. 시도 선택
        select = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'do_code1'))
        )
        select = Select(select)
        select.select_by_index(1)

        # 2. 시군구 선택
        select_1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'city_code1'))
        )
        select_1 = Select(select_1)
        select_1.select_by_index(1)

        # 3. 읍면동 선택
        select_2 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'dong_code1'))
        )
        select_2 = Select(select_2)
        select_2.select_by_index(1)

        # 4. 빠른검색 입력
        search_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "searchInput"))
        )
        search_input.send_keys("상봉동 동부아파트")

        # 5. 검색 결과 클릭
        quick_search_result = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "quickSearchResult"))
        )
        quick_search_result.click()

        # 6. 더보기 클릭
        map_pop_info_bottom_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "map_pop_info_bottom_btn"))
        )
        map_pop_info_bottom_btn.click()

        # 7. 팝업창으로 창 전환
        driver.switch_to.window(driver.window_handles[1])

        # 8. 팝업 내 '호별 시세조회' 요소 클릭
        ho_background = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//span[text()="호별 시세조회"]'))
        )
        driver.execute_script("arguments[0].click();", ho_background)

        # 9. 동, 호수 선택
        select_dong = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'dong_'))
        )
        select_dong = Select(select_dong)
        select_dong.select_by_index(1)

        select_ho = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'ho_'))
        )
        select_ho = Select(select_ho)
        select_ho.select_by_index(1)

        # # 10. 보안문자 (캡차 이미지 다운로드)
        # # 보안문자 (캡차 이미지 다운로드 스크린샷 방식)
        # captcha_img = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.ID, "captchaImg"))
        # )

        # # 전체 페이지 스크린샷 찍기
        # screenshot_path = os.path.join(save_path, "full_screenshot.png")
        # driver.save_screenshot(screenshot_path)
        
        # # 캡차 이미지의 위치 및 크기 가져오기
        # location = captcha_img.location
        # size = captcha_img.size
        # # 캡차 이미지 위치 및 크기 출력 (디버깅용)
        # print(f"캡차 이미지 위치: {location}")
        # print(f"캡차 이미지 크기: {size}")
                

        # # PIL로 스크린샷을 열어 위치에 따라 캡차 이미지를 자르기
        # with Image.open(screenshot_path) as img:
        #     left = location['x'] + 149
        #     top = location['y'] + 90
        #     right = left + size['width']
        #     bottom = top + size['height']
            
        #     captcha = img.crop((left, top, right, bottom))

        #     # 캡차 이미지 파일명 생성
        #     captcha_filename = os.path.join(save_path, f"captcha_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
        #     captcha.save(captcha_filename)
        #     print(f"캡차 이미지 {captcha_filename} 다운로드 완료")

        # 마지막 대기
        time.sleep(2)

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
