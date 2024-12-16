from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time
import os

def wetax_officetel(driver):
    url = "https://www.wetax.go.kr/tcp/loi/J030401M01.do"
    driver.get(url)

    time.sleep(5)

    # 관할 자치단체 선택
    ctpv_cd = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "ctpvCd")))
    select = Select(ctpv_cd)
    select.select_by_visible_text("경상남도")
    time.sleep(3)

    sgg_cd = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "sggCd")))
    select = Select(sgg_cd)
    select.select_by_visible_text("김해시")
    time.sleep(3)

    stdg_cd = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "stdgCd")))
    select = Select(stdg_cd)
    select.select_by_visible_text("내동")
    time.sleep(3)

    # 기준연도 선택
    aplcn_yr = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "aplcnYr")))
    Select(aplcn_yr).select_by_index(1)
    time.sleep(3)

    # 특수번지 선택
    srg_cd = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "srgCd")))
    Select(srg_cd).select_by_index(1)
    time.sleep(3)

    # 본번지 입력
    txt_exst_prlno = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "txtExstPrlno")))
    txt_exst_prlno.send_keys("1136")
    txt_exst_prlno.send_keys(Keys.ENTER)
    time.sleep(3)

    # 부번지 입력
    bsno = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bsno")))
    bsno.send_keys("4")
    bsno.send_keys(Keys.ENTER)
    time.sleep(3)

    # 건물 동 입력
    bsno = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bldgDaddr")))
    bsno.send_keys("")
    bsno.send_keys(Keys.ENTER)
    time.sleep(3)

    # 건물 호 입력
    bsno = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bldgHoadr")))
    bsno.send_keys("1301")
    bsno.send_keys(Keys.ENTER)
    time.sleep(3)

    # 검색 버튼 클릭
    btn_srch_blds_cpb = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnSrchBldsCpb")))
    btn_srch_blds_cpb.click()

    time.sleep(3)

    # <td> 또는 <span> 요소 찾기
    span_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//td[@class='a-r']/span[@class='roboto']"))
    )
    
    # 텍스트 값 가져오기
    raw_text = span_element.text.strip()  # 예: '82,198,449'
    # 쉼표 제거 및 숫자로 변환
    numeric_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {numeric_value}")  # 출력: 82198449
    
    return numeric_value 


