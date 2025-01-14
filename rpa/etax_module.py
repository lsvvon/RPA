from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import TimeoutException

def etax_officetel(driver, **kwargs):
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

    url = "https://etax.seoul.go.kr"
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
    SIGU_CD.select_by_visible_text(Sigungu)
    time.sleep(3)

    # 법정동
    hDONG = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "HDONG260")))
    HDONG = Select(hDONG)
    HDONG.select_by_visible_text(Ridong)
    time.sleep(3)

    # 특수지
    tsj_gubun = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "tsj_gubun")))
    Tsj_gubun = Select(tsj_gubun)
    Tsj_gubun.select_by_visible_text("일반번지")
    time.sleep(3)

    # 본번지
    bonbun = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bonbun")))
    bonbun.send_keys(Jibun_No1)
    time.sleep(3)

    # 부번지
    bubun = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "bubun")))
    bubun.send_keys(Jibun_No2)
    time.sleep(3)

    # 동
    dong = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "dong")))
    dong.send_keys(Building_No1)
    time.sleep(3)

    # 호
    hosu = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "hosu")))
    hosu.send_keys(Room_No)
    time.sleep(3)

    # 조회 클릭
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "black"))
    )
    driver.execute_script("searchB();", search_button)

    time.sleep(3)

    # XPath로 "69,767,826 원" 값이 있는 <td> 요소 찾기
    td_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//tr/td[@class='right' and not(contains(@class, 'last'))]"))
    )
    
    # 텍스트 값 추출
    raw_text = td_element.text.strip()  # '69,767,826 원' 형태
    
    # 쉼표와 단위 제거 및 숫자 변환
    etax_value = int(raw_text.replace(",", "").replace(" 원", ""))
    print(f"Numeric value: {etax_value}")  # 출력: 69767826
    
    return etax_value





    

