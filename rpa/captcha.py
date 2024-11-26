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
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from PIL import Image
import time

# SSL 인증서 검증 무시 설정
ssl._create_default_https_context = ssl._create_unverified_context

# 캡차 이미지 저장 경로 설정
save_path = r"C:\시세조사\캡챠"
if not os.path.exists(save_path):
    os.makedirs(save_path)

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)
url = "https://rtech.or.kr/main/mapSearch.do?popUpYn=&posX=37.48243936583027&posY=127.06183029780048"
driver.get(url)

# 캡차 이미지 수집 횟수 설정
capture_count = 219

for attempt in range(capture_count):
    try:
        # 1. 팝업 내 '호별 시세조회' 요소 클릭
        ho_background = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//span[text()="호별 시세조회"]'))
        )
        driver.execute_script("arguments[0].click();", ho_background)

        # 2. 보안문자 (캡차 이미지 다운로드)
        captcha_img = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "captchaImg"))
        )

        # 전체 페이지 스크린샷 찍기
        screenshot_path = os.path.join(save_path, f"full_screenshot.png")
        driver.save_screenshot(screenshot_path)

        # 캡차 이미지의 위치 및 크기 가져오기
        location = captcha_img.location
        size = captcha_img.size

        # PIL로 스크린샷을 열어 위치에 따라 캡차 이미지를 자르기
        with Image.open(screenshot_path) as img:
            left = location['x'] + 195
            top = location['y'] + 90
            right = left + size['width']
            bottom = top + size['height']
            
            captcha = img.crop((left, top, right, bottom))

            # 캡차 이미지 파일명 생성
            captcha_filename = os.path.join(save_path, f"captcha_image_{datetime.now().strftime('%Y%m%d%H%M%S')}_{attempt + 1}.png")
            captcha.save(captcha_filename)
            print(f"{attempt + 1}번째 캡차 이미지 {captcha_filename} 다운로드 완료")

        # 새로고침 후 다음 캡차 이미지 로드 대기
        driver.refresh()
        time.sleep(3)  # 새로고침 후 페이지 로드 대기

    except TimeoutException as e:
        print(f"타임아웃 발생: {e}, 다음 시도로 진행...")
        driver.quit()  
        driver = webdriver.Chrome(options=options)  # 새로 드라이버를 열어 다시 시도
        driver.get(url)
        
print("캡차 이미지 수집 완료")
driver.quit()

