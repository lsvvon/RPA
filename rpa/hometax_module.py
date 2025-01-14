from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support.select import Select
import ssl

# SSL 인증서 검증 무시 설정
ssl._create_default_https_context = ssl._create_unverified_context

def hometax_streetnum(driver, **kwargs):
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
    search_input.send_keys("기준시가조회")
    time.sleep(1)
    search_input.send_keys(Keys.RETURN)  # 엔터 키 입력
    
    # 오피스텔 및 상업용 건물 클릭
    office_building = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@id='mf_txppWframe_menu_gen_0_tbx_content' and contains(@class, 'w2textbox')]"))
    )
    office_building.click() 
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
    input_element.send_keys(Ridong)
    time.sleep(3)

    # 조회 클릭
    select_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "mf_txppWframe_UTECMAAA08_wframe_trigger6"))
    )
    driver.execute_script("arguments[0].click();", select_button)
    time.sleep(3)

    # 모든 행을 가져오기
    rows = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//table//tr'))
    )
    for row in rows:
        try:
            # 각 행에서 "구" 텍스트를 찾기
            if Sigungu in row.text:
                # 해당 행의 "선택" 버튼 클릭
                select_button = row.find_element(By.XPATH, './/button[@title="선택"]')
                select_button.click()
                break
        except Exception as e:
            # 행에 "선택" 버튼이 없을 경우를 대비한 예외 처리
            print(f"오류 발생: {e}")
    
    time.sleep(3)
    # 번지/호 입력
    mf_txppWframe_txtBunj = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "mf_txppWframe_txtBunj"))
    )
    mf_txppWframe_txtBunj.send_keys(Jibun_No1)

    # 번지/호 입력
    mf_txppWframe_txtHo = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "mf_txppWframe_txtHo"))
    )
    mf_txppWframe_txtHo.send_keys(Jibun_No2)
    time.sleep(3)

    # 검색버튼 클릭
    select_button2= WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnSchBld"))
    )
    driver.execute_script("arguments[0].click();", select_button2)
    time.sleep(5)

    # 해당 물건지 찾기
    try:
        # 모든 표시된 `txtItm` 요소 찾기
        visible_items = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//li[not(contains(@style, 'display: none;'))]//a[starts-with(@id, 'txtItm')]")
            )
        )

        # 각 요소의 텍스트 확인
        for item in visible_items:
            item_text = item.text.strip()
            print(f"찾은 항목 텍스트: {item_text}")

            if Building_Name in item_text:
                print(f"목표 항목 '{Building_Name}'를 찾았습니다. 클릭합니다.")
                driver.execute_script("arguments[0].scrollIntoView();", item)
                item.click()
                break

            print(f"목표 항목 '{Building_Name}'를 찾지 못했습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")
        return False

    # 상세주소 검색
    # 동
    select_dong = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldComp'))
    )
    select = Select(select_dong)
    if not Building_No1 or Building_No1.strip() == "": # Building_No1이 빈값인지 확인
        # 첫 번째 옵션 선택
        select.select_by_index(0)
        print("Building_No1이 빈값이므로 첫 번째 옵션을 선택했습니다.")
    else:
        # Building_No1 값으로 선택
        try:
            select.select_by_visible_text(Building_No1)
            print(f"'{Building_No1}' 값으로 선택했습니다.")
        except Exception as e:
            print(f"'{Building_No1}' 값으로 선택하는 데 실패했습니다: {e}")

    # 층
    select_floor = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldFlor'))
    )
    select_1 = Select(select_floor)
    select_1.select_by_visible_text(Building_No1)

    # 호
    select_ho = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldHo'))
    )
    select_2 = Select(select_ho)
    select_2.select_by_visible_text(Room_No)

    # 검색버튼 클릭
    mf_txppWframe_btnSchTsv= WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnSchTsv"))
    )
    driver.execute_script("arguments[0].click();", mf_txppWframe_btnSchTsv)
    time.sleep(5)

    # 1. 첫 번째 값 (4,761,000)
    price_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='notcPrc']/nobr"))
    )
    raw_price = price_element.text.strip()  # '4,761,000'
    hometax_price_value = int(raw_price.replace(",", ""))  # 쉼표 제거 후 숫자로 변환

    # 2. 두 번째 값 (36.4)
    size_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='bldTotaSfl']/nobr"))
    )
    raw_size = size_element.text.strip()  # '36.4'
    hometax_size_value = float(raw_size)  # 실수로 변환

    print(f"Price: {hometax_price_value}, Size: {hometax_size_value}")

    return hometax_price_value, hometax_size_value


def hometax_roadnum(driver, **kwargs):
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
    search_input.send_keys("기준시가조회")
    time.sleep(1)
    search_input.send_keys(Keys.RETURN)  # 엔터 키 입력
    
    # 오피스텔 및 상업용 건물 클릭
    office_building = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@id='mf_txppWframe_menu_gen_0_tbx_content' and contains(@class, 'w2textbox')]"))
    )
    office_building.click() 
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

    # 해당 물건지 찾기
    try:
        # 모든 표시된 `txtRdNmItm0` 요소 찾기
        visible_items = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//li[not(contains(@style, 'display: none;'))]//a[starts-with(@id, 'txtRdNmItm')]")
            )
        )

        # 각 요소의 텍스트 확인
        for item in visible_items:
            item_text = item.text.strip()
            print(f"찾은 항목 텍스트: {item_text}")

            if Doro_Name in item_text:
                print(f"목표 항목 '{Doro_Name}'를 찾았습니다. 클릭합니다.")
                driver.execute_script("arguments[0].scrollIntoView();", item)
                item.click()
                break

            print(f"목표 항목 '{Doro_Name}'를 찾지 못했습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")
        return False

    time.sleep(3)

    # 해당 오피스텔 클릭
    try:
        # 모든 표시된 `txtItm` 요소 찾기
        visible_items = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//li[not(contains(@style, 'display: none;'))]//a[starts-with(@id, 'txtItm')]")
            )
        )

        # 각 요소의 텍스트 확인
        for item in visible_items:
            item_text = item.text.strip()
            print(f"찾은 항목 텍스트: {item_text}")

            if Building_Name in item_text:
                print(f"목표 항목 '{Building_Name}'를 찾았습니다. 클릭합니다.")
                driver.execute_script("arguments[0].scrollIntoView();", item)
                item.click()
                break

            print(f"목표 항목 '{Building_Name}'를 찾지 못했습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")
        return False

    time.sleep(3)
    # 상세주소 검색
     # 동
    select_dong = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldComp'))
    )
    select = Select(select_dong)
    if not Building_No1 or Building_No1.strip() == "":  # Building_No1이 빈값인지 확인
        # 첫 번째 옵션 선택
        select.select_by_index(0)
        print("Building_No1이 빈값이므로 첫 번째 옵션을 선택했습니다.")
    else:
        # Building_No1 값으로 선택
        try:
            select.select_by_visible_text(Building_No1)
            print(f"'{Building_No1}' 값으로 선택했습니다.")
        except Exception as e:
            print(f"'{Building_No1}' 값으로 선택하는 데 실패했습니다: {e}")
    
    # 층
    select_floor = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldFlor'))
    )
    select_1 = Select(select_floor)
    select_1.select_by_visible_text(Building_No1)

    # 호
    select_ho = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldHo'))
    )
    select_2 = Select(select_ho)
    select_2.select_by_visible_text(Room_No)

    # 검색버튼 클릭
    mf_txppWframe_btnSchTsv= WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnSchTsv"))
    )
    driver.execute_script("arguments[0].click();", mf_txppWframe_btnSchTsv)
    time.sleep(5)

    # 1. 첫 번째 값 (4,761,000)
    price_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='notcPrc']/nobr"))
    )
    raw_price = price_element.text.strip()  # '4,761,000'
    hometax_price_value = int(raw_price.replace(",", ""))  # 쉼표 제거 후 숫자로 변환

    # 2. 두 번째 값 (36.4)
    size_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='bldTotaSfl']/nobr"))
    )
    raw_size = size_element.text.strip()  # '36.4'
    hometax_size_value = float(raw_size)  # 실수로 변환

    print(f"Price: {hometax_price_value}, Size: {hometax_size_value}")
    
    return hometax_price_value, hometax_size_value


