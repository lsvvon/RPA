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
from selenium.webdriver.support.select import Select

# 최대 시도 횟수 설정
MAX_RETRIES = 3
attempt = 0
#building = "공동주택"
building = "개별주택"

while attempt < MAX_RETRIES:
    try:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        driver = webdriver.Chrome(options=options)
        url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
        driver.get(url)

        # 페이지 로드가 완료될 때까지 기다리기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 현재 창 정보
        main_window = driver.current_window_handle

        # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
        for window in driver.window_handles:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()


        # 메인 창으로 전환
        driver.switch_to.window(main_window)

        # 공동주택(아파트, 다세대)일 경우
        if building == "공동주택" : 
            # "표준단독주택공시가격"으로 이동
            link_element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//img[@alt='표준단독주택공시가격']"))
            )
            link_element.click() 

            zibun_search = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//img[@alt='지번검색']"))
            )
            zibun_search.click() 

            time.sleep(3)

            # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
            sido_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sido_list'))
            )
            select = Select(sido_list)
            select.select_by_visible_text("서울특별시")

            time.sleep(3)
            sgg_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sgg_list'))
            )
            select_1 = Select(sgg_list)
            select_1.select_by_visible_text("송파구")

            time.sleep(3)
            eub_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'eub_list'))
            )
            select_2 = Select(eub_list)
            select_2.select_by_visible_text("가락동")

            time.sleep(3)
            # '검색' 버튼 가져오기
            search_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='image' and @alt='검색']"))
            )

            # 버튼 클릭
            search_button.click()

            time.sleep(3)

            # 저장할 폴더 경로 지정
            folder_path = r"C:\python\RPA\rpa\realtyprice_capImg"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # 파일 경로 설정
            screenshot_path = os.path.join(folder_path, "full_page_screenshot.png")
            full_screenshot.capture_full_page(driver, screenshot_path)
            print(f"전체 페이지 스크린샷 저장 완료: {screenshot_path}")
        
        elif building == "개별주택":
            # "개별단독주택이서ㅇ"으로 이동
            link_element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//img[@alt='개별단독주택공시가격']"))
            )
            link_element.click() 

            zibun_search = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//img[@alt='지번검색']"))
            )
            zibun_search.click() 

            time.sleep(3)

            # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
            sido_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sido_list'))
            )
            select = Select(sido_list)
            select.select_by_visible_text("서울특별시")

            time.sleep(3)
            sgg_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sgg_list'))
            )
            select_1 = Select(sgg_list)
            select_1.select_by_visible_text("송파구")

            time.sleep(3)
            eub_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'eub_list'))
            )
            select_2 = Select(eub_list)
            select_2.select_by_visible_text("가락동")



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
