from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import urllib.request
import time
import os

def etax_officetel(driver):
    url = "https://etax.seoul.go.kr"
    driver.get(url)

    time.sleep(5)

    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()
            

    # Switch to iframe
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)

    all_menu = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "all_menu"))
    )
    all_menu.click()

    time.sleep(3)

    # 조회/발급 클릭
    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "조회/발급"))
    )
    driver.execute_script("goMenuByMenuID('0709');", link)

    time.sleep(3)

    # 주택외건물시가 표준액조회 클릭
    link_1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "주택외건물시가 표준액조회"))
    )
    driver.execute_script("lnbMenuPage2('0709', 'BldnStndAmtLstAction.view', '_self');", link_1)

    time.sleep(3)

    # 상세주소 입력 후 조회 클릭
    # 년도
    gWAPO_YEAR = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "GWAPO_YEAR")))
    Select(gWAPO_YEAR).select_by_index(1)
    time.sleep(3)

    # 관할구청
    sIGU_CD = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "SIGU_CD")))
    SIGU_CD = Select(sIGU_CD)
    SIGU_CD.select_by_visible_text("중랑구")
    time.sleep(3)

    # 법정동
    hDONG = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "HDONG260")))
    HDONG = Select(hDONG)
    HDONG.select_by_visible_text("신내동")
    time.sleep(3)

    # 특수지
    tsj_gubun = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "tsj_gubun")))
    Tsj_gubun = Select(tsj_gubun)
    Tsj_gubun.select_by_visible_text("일반번지")
    time.sleep(3)

    # 본번지
    bonbun = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bonbun")))
    bonbun.send_keys("835")
    time.sleep(3)

    # 부번지
    bubun = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bubun")))
    bubun.send_keys("")
    time.sleep(3)

    # 동
    dong = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "dong")))
    dong.send_keys("102")
    time.sleep(3)

    # 호
    hosu = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "hosu")))
    hosu.send_keys("707")
    time.sleep(3)

    # 조회 클릭
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "black"))
    )
    driver.execute_script("searchB();", search_button)

    time.sleep(3)





    

