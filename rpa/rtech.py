import ssl
import os
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
import urllib.request as req
import ssl
from io import BytesIO
import predict_sh

# SSL 인증서 검증 무시 설정
ssl._create_default_https_context = ssl._create_unverified_context

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
        # 현재 창 정보
        main_window = driver.current_window_handle

        # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
        for window in driver.window_handles:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()

                
        # 1. 시도 선택
        select = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'do_code1'))
        )
        select = Select(select)
        select.select_by_index(5)

        # 2. 시군구 선택
        select_1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'city_code1'))
        )
        select_1 = Select(select_1)
        select_1.select_by_index(5)

        # 3. 읍면동 선택
        select_2 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, 'dong_code1'))
        )
        select_2 = Select(select_2)
        select_2.select_by_index(12)

        # 4. 빠른검색 입력
        search_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "searchInput"))
        )
        search_input.send_keys("에드가리움 2차")

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
        # select_dong = WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.NAME, 'dong_'))
        # )
        # select_dong = Select(select_dong)
        # select_dong.select_by_index(1)
        
        select_ho_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'office_ho_code'))
        )
     
        # 드롭다운의 옵션 가져오기
        select_ho = Select(select_ho_element)
        time.sleep(2)
        # "601호"에 해당하는 옵션을 선택
        desired_text = "오피스텔 601호"
        options = select_ho.options  # 드롭다운의 모든 옵션

        for index, option in enumerate(options):
            if desired_text.strip() == option.text:  # 원하는 텍스트가 포함된 경우
                select_ho.select_by_index(index)  # 해당 옵션 선택
                break
        else:
            print(f"'{desired_text}'에 해당하는 호 옵션을 찾을 수 없습니다.")

        # 10. 보안문자 (캡차 이미지 다운로드)
        # 보안문자 (캡차 이미지 다운로드 스크린샷 방식)
        # 전체 페이지의 사이즈를 구하여 브라우저의 창 크기를 확대하고 스크린캡처를 합니다.

        save_path = r"C:\python\RPA\rpa\captcha_images_save"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        page_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        page_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(page_width, page_height)
        png = driver.get_screenshot_as_png()

        captcha_img = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "office_captchaImg"))
        )

        element = captcha_img
        image_location = element.location
        image_size = element.size
        
        # 이미지를 element의 위치에 맞춰서 crop 하고 저장합니다.
        im = Image.open(BytesIO(png))
        left = image_location['x']
        top = image_location['y']
        right = image_location['x'] + image_size['width']
        bottom = image_location['y'] + image_size['height']
        im = im.crop((left, top, right, bottom))

        captcha_filename = os.path.join(save_path, "capcha.png")
        im.save(captcha_filename)

        captcha_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "office_capcha"))
        )
        time.sleep(5)

        captcha_input.send_keys(predict_sh.get_predictions())

        # 11. 확인 버튼 누른 뒤 화면 캡쳐하기
        confirm_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@onclick='javascript:office_search_dongho_price()']"))
        )
        confirm_button.click()
        time.sleep(5)

        # 저장할 폴더 경로 지정
        folder_path = r"C:\python\RPA\rpa\rtech_capImg"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 파일 경로 설정
        screenshot_path = os.path.join(folder_path, "full_page_screenshot.png")
        driver.save_screenshot(screenshot_path)

        # 마지막 대기
        time.sleep(10)

        # 캡처 완료 후 루프를 탈출하도록 시도 횟수를 최대값으로 설정
        attempt = MAX_RETRIES

    except TimeoutException as e:
        print(f"타임아웃 발생: {e}, 재시도 중...")
        attempt += 1
        driver.quit()  # 타임아웃 발생 시 드라이버 종료 후 새로 시도

    finally:
        if attempt >= MAX_RETRIES:
            print("프로그램 종료.")
            driver.quit()
