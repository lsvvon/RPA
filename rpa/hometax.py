from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support.select import Select
import os
import full_screenshot

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
        url = "https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&menuCd=index2"
        driver.get(url)
        
        time.sleep(10)

        # 페이지 로드가 완료될 때까지 기다리기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 덮고 있는 요소가 사라질 때까지 대기
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.ID, "mf_wq_uuid_24_mf_wq_uuid_24_wq_proessMsgModal"))
        )

        # 검색창에 기준시가 입력
        search_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "w2input"))
        )
        search_input.click()
        search_input.send_keys("기준시가")
        time.sleep(5)
        
        # 오피스텔 및 상업용 건물 클릭
        office_building = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='오피스텔 및 상업용 건물']"))
        )
        driver.execute_script("arguments[0].click();", office_building)
        time.sleep(5)

        # 법정동검색 클릭
        txppWframe_button = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnLdCdPop"))
        )
        txppWframe_button.click()
        time.sleep(5)

        # 읍면동,가리 입력 
        input_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "mf_txppWframe_UTECMAAA08_wframe_inputSchNm"))
        )
        input_element.send_keys("독산동")

        # 조회 클릭
        select_button = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "mf_txppWframe_UTECMAAA08_wframe_trigger6"))
        )
        driver.execute_script("arguments[0].click();", select_button)

        # 선택 클릭
        select_button1= WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='선택']"))
        )
        driver.execute_script("arguments[0].click();", select_button1)
        time.sleep(5)

        # 번지/호 입력
        mf_txppWframe_txtBunj = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "mf_txppWframe_txtBunj"))
        )
        mf_txppWframe_txtBunj.send_keys("301")

        # 번지/호 입력
        mf_txppWframe_txtHo = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "mf_txppWframe_txtHo"))
        )
        mf_txppWframe_txtHo.send_keys("23")
        
        # 검색버튼 클릭
        select_button2= WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnSchBld"))
        )
        driver.execute_script("arguments[0].click();", select_button2)
        time.sleep(5)

        # 물건지 클릭
        txtItm0= WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "txtItm0"))
        )
        driver.execute_script("arguments[0].click();", txtItm0)
        time.sleep(5)

        # 상세주소 검색
        select_dong = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldComp'))
        )
        select = Select(select_dong)
        select.select_by_index(1)
        
        select_floor = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldFlor'))
        )
        select_1 = Select(select_floor)
        select_1.select_by_index(11)
      
        select_ho = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldHo'))
        )
        select_2 = Select(select_ho)
        select_2.select_by_index(1)

        # 검색버튼 클릭
        mf_txppWframe_btnSchTsv= WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnSchTsv"))
        )
        driver.execute_script("arguments[0].click();", mf_txppWframe_btnSchTsv)
        time.sleep(5)

        
        # 저장할 폴더 경로 지정
        folder_path = r"C:\python\RPA\rpa\hometax_capImg"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 파일 경로 설정
        screenshot_path = os.path.join(folder_path, "full_page_screenshot.png")
        full_screenshot.capture_full_page(driver, screenshot_path)
        print(f"전체 페이지 스크린샷 저장 완료: {screenshot_path}")

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
