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
from bs4 import BeautifulSoup 

import cv2
import re
import requests
import numpy as np
import urllib.request as req

from io import BytesIO
# from selenium.webdriver.firefox.options import Options

# SSL 인증서 검증 무시 설정
ssl._create_default_https_context = ssl._create_unverified_context

# 캡차 이미지 저장 경로 설정
save_path = r"C:\Python\시세조사\캡챠"
if not os.path.exists(save_path):
    os.makedirs(save_path)

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)
url = "https://rtech.or.kr/MarketPrice/getMarketPriceDetail.do?categoryCd=1&aptSeq=2410&addrCode=1126010200&price_info=1"
driver.get(url)


# 1. 팝업 내 '호별 시세조회' 요소 클릭
ho_background = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, '//span[text()="호별 시세조회"]'))
)
driver.execute_script("arguments[0].click();", ho_background)

# 2. 보안문자 (캡차 이미지 다운로드)
captcha_img = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "captchaImg"))
)


# 캡차 이미지 수집 횟수 설정
capture_count = 1

for attempt in range(capture_count):
    try:
      
        # url = captcha_img.get_attribute('src')
        # img = requests.get(src).content
        # print(url)
        '''
        url = "https://rtech.or.kr/common/captchaImg.do;jsessionid=CA38695943CD1078721C0C892E81B60A"

        captcha_filename = os.path.join(save_path, f"captcha_image_{datetime.now().strftime('%Y%m%d%H%M%S')}_{attempt + 1}.png")
        req.urlretrieve(url, captcha_filename)
        print(f"{attempt + 1}번째 캡차 이미지 {captcha_filename} 다운로드 완료")
        '''
        
        # 전체 페이지의 사이즈를 구하여 브라우저의 창 크기를 확대하고 스크린캡처를 합니다.
        page_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        page_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(page_width, page_height)
        png = driver.get_screenshot_as_png()
        
        # find_element_ 나 find_elements_ 속성의 하위 메서드를 사용하시는 분들은 전부
        # find_element/find_elements 메서드로 대체해서 사용하시길 바랍니다.

        # 특정 element의 위치를 구하고 selenium 창을 닫습니다.
        element = captcha_img

        image_location = element.location
        image_size = element.size
        # driver.quit()

        # 이미지를 element의 위치에 맞춰서 crop 하고 저장합니다.
        im = Image.open(BytesIO(png))
        left = image_location['x']
        top = image_location['y']
        right = image_location['x'] + image_size['width']
        bottom = image_location['y'] + image_size['height']
        im = im.crop((left, top, right, bottom))

        captcha_filename = os.path.join(save_path, f"captcha_image_{datetime.now().strftime('%Y%m%d%H%M%S')}_{attempt + 1}.png")
        im.save(captcha_filename)

        '''
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
        '''

        # 새로고침 후 다음 캡차 이미지 로드 대기
        # driver.refresh()
        time.sleep(60)  # 새로고침 후 페이지 로드 대기
        # driver.execute_script("javascript:captchaReload()")
        # <button onclick="javascript:captchaReload()">새로고침</button>

    except TimeoutException as e:
        print(f"타임아웃 발생: {e}, 다음 시도로 진행...")
        driver.quit()  
        driver = webdriver.Chrome(options=options)  # 새로 드라이버를 열어 다시 시도
        driver.get(url)
        
print("캡차 이미지 수집 완료")
driver.quit()
