from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium.common.exceptions import TimeoutException


def wetax_officetel(driver, **kwargs):
    # 주소 값 가져오기
    Sido = kwargs.get('Sido1')
    Sigungu = kwargs.get('Sigungu1')
    Ridong = kwargs.get('Ridong1')
    Jibun_No1 = kwargs.get('Jibun_No1')
    Jibun_No2 = kwargs.get('Jibun_No2')
    Building_Name = kwargs.get('Building_Name1')
    Building_No1 = kwargs.get('Building_No1')
    Building_No2 = kwargs.get('Building_No2')
    Room_No = kwargs.get('Room_No1')
    Doro_Name = kwargs.get('Doro_Name1')
    Chosung = kwargs.get('Chosung1')

    url = "https://www.wetax.go.kr/tcp/loi/J030401M01.do"
    driver.get(url)

    time.sleep(5)
    try:
        # iframe 내로 전환
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        # 닫기 버튼을 찾기 위한 XPath
        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='닫기' and contains(@style, 'position: absolute')]"))
        )
        # 버튼 클릭
        driver.execute_script("arguments[0].click();", close_button)
        print("팝업 닫기 버튼 클릭 완료.")
        # iframe에서 메인 페이지로 돌아가기
        driver.switch_to.default_content()
    except TimeoutException:
        print("모달 닫기 버튼이 존재하지 않음.")
        driver.switch_to.default_content()
    except Exception as e:
        print(f"팝업 닫기 버튼 클릭 중 예외 발생: {e}")
        driver.switch_to.default_content()
    

    # 관할 자치단체 선택
    ctpv_cd = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "ctpvCd")))
    select = Select(ctpv_cd)
    select.select_by_visible_text(Sido)
    time.sleep(3)

    sgg_cd = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "sggCd")))
    select = Select(sgg_cd)
    select.select_by_visible_text(Sigungu)
    time.sleep(3)

    stdg_cd = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "stdgCd")))
    select = Select(stdg_cd)
    select.select_by_visible_text(Ridong)
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
    txt_exst_prlno.send_keys(Jibun_No1)
    txt_exst_prlno.send_keys(Keys.ENTER)
    time.sleep(3)

    # 부번지 입력
    bsno = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bsno")))
    bsno.send_keys(Jibun_No2)
    bsno.send_keys(Keys.ENTER)
    time.sleep(3)

    # 건물 동 입력
    bsno = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bldgDaddr")))
    bsno.send_keys(Building_No1)
    bsno.send_keys(Keys.ENTER)
    time.sleep(3)

    # 건물 호 입력
    bsno = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bldgHoadr")))
    bsno.send_keys(Room_No)
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
    wetax_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {wetax_value}")  # 출력: 82198449
    
    return wetax_value 


