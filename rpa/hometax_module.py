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

def hometax_streetnum(driver):
    url = "https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&menuCd=index2"
    driver.get(url)

    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()

    
    time.sleep(10)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # 덮고 있는 요소가 사라질 때까지 대기
    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located((By.ID, "mf_wq_uuid_24_mf_wq_uuid_24_wq_proessMsgModal"))
    )
    time.sleep(5)

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
    time.sleep(3)

    # 조회 클릭
    select_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "mf_txppWframe_UTECMAAA08_wframe_trigger6"))
    )
    driver.execute_script("arguments[0].click();", select_button)
    time.sleep(3)

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
    time.sleep(3)

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

def hometax_roadnum(driver):
    url = "https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&menuCd=index2"
    driver.get(url)

    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()

    
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

    # 도로명주소로 조회 클릭
    raod_click = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='mf_txppWframe_rdoByRoadNmCd_input_0']"))
    )
    # 요소 클릭
    raod_click.click()
    time.sleep(3)

    # 도로명주소 입력
    mf_txppWframe_txtRoadNm = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "mf_txppWframe_txtRoadNm"))
    )
    mf_txppWframe_txtRoadNm.send_keys("문래북로")
    time.sleep(3)

    # 검색 클릭
    mf_txppWframe_btnSchRoadNm= WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnSchRoadNm"))
    )
    driver.execute_script("arguments[0].click();", mf_txppWframe_btnSchRoadNm)
    time.sleep(5)

    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[text()='서울특별시 영등포구 당산동1가 문래북로']"))
    )
    # 클릭 실행
    element.click()
    time.sleep(5)

    # 해당 오피스텔 클릭
    item = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[text()='디아인스']"))
    )
    item.click()

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
    select_1.select_by_index(1)

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

