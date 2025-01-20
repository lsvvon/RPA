from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException

# 공동주택(아파트, 다세대)일 경우 - 지번 검색
def realtyprice_apt_streetnum(driver, **kwargs):
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

    print("지번2:", Jibun_No2)
    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    try:
        # 팝업 div이 포함된 iframe으로 전환
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#wrap_pop_no iframe.b-iframe"))
        )
        driver.switch_to.frame(iframe)

        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@onclick, 'closeWin')]"))
        )
        driver.execute_script("arguments[0].click();", close_button)
        # iframe에서 메인 페이지로 돌아가기
        driver.switch_to.default_content()
        time.sleep(1)  # 버튼 클릭 후 잠시 대기

    except TimeoutException:
        print("모달 닫기 버튼이 존재하지 않음.")
        driver.switch_to.default_content()
    except Exception as e:
        print(f"모달 닫기 중 예외 발생: {e}")
        driver.switch_to.default_content()
    

    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()


    # 메인 창으로 전환
    driver.switch_to.window(main_window)

    # "표준단독주택공시가격"으로 이동
    link_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='공동주택공시가격']"))
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
    select.select_by_visible_text(Sido)

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sgg_list'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text(Sigungu)

    time.sleep(3)
    eub_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'eub_list'))
    )
    select_2 = Select(eub_list)
    select_2.select_by_visible_text(Ridong)

    time.sleep(3)
    
    # 지번 입력 클릭
    radio_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='rdoCondi' and @value='1']"))
    )
    driver.execute_script("arguments[0].click();", radio_button)

    time.sleep(3)

    # 번지 입력
    bun1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun1' and @class='text2']"))
    )
    driver.execute_script("arguments[0].click();", bun1)
    bun1.send_keys(Jibun_No1)

    time.sleep(3)

    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun2' and @class='text2']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys(Jibun_No2)

    time.sleep(3)

    # 검색 클릭            
    search_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@class, 'btn-src1')]"))
    )
    driver.execute_script("searchAptName(1);", search_button)

    if bun2.get_attribute("value") == '0':
        # 검색 클릭            
        search_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@class, 'btn-src1')]"))
        )
        driver.execute_script("searchAptName(1);", search_button)

    time.sleep(3)

    # 단지명 클릭
    apt = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'apt'))
    )
    select_3 = Select(apt)
    for option in select_3.options:
        print(select_3.options)
        if Building_Name in option.text:  # Building_Name이 포함된 텍스트를 찾음
            print(option.text)
            select_3.select_by_visible_text(option.text)
            break

    time.sleep(3)

    # 동 클릭
    dong = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'dong'))
    )
    select_4 = Select(dong)
    # Building_No1이 빈값인지 확인
    if not Building_No1 or Building_No1.strip() == "":
        print("Building_No1 값이 비어 있습니다. 동명없음 선택")
        select_4.select_by_index(0)  # 첫 번째 값 선택
    else:
        select_4.select_by_visible_text(Building_No1) 

    time.sleep(3)
    # 호 클릭
    ho = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'ho'))
    )
    select_5 = Select(ho)
    select_5.select_by_visible_text(Room_No)

    time.sleep(3)

    # 열람하기 클릭
    show_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@class, 'btn-src3')]"))
    )
    driver.execute_script("goPage('1')", show_button)

    time.sleep(3)

    # 공동주택가격 값
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "opinNoticeAmt"))
    )
    
    # 값 추출 및 공백 제거
    raw_text = element.text.strip()
    print(f"Raw value: {raw_text}")  # 출력: '211,000,000'
    
    # 쉼표 제거 및 숫자로 변환
    realty_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {realty_value}")  # 출력: 211000000

    # 전용면적 값
    element_1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#dataList tr:first-child td:nth-child(5)"))
    )
    
    # 값 추출 및 공백 제거
    element_1_text = element_1.text.strip()
    print(f"element_1_text: {element_1_text}") 
    
    # 쉼표 제거 및 숫자로 변환
    area_value = float(element_1_text.replace(",", ""))
    print(f"area_value: {area_value}") 

    # 기준일 값
    date_element = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, "//tbody[@id='dataList']/tr[1]/td[1]"))
    )

    date_value = date_element.text

    return [realty_value, 0, area_value, date_value]

def realtyprice_apt_roadnum(driver, **kwargs):
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

    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    try:
        # 팝업 div이 포함된 iframe으로 전환
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#wrap_pop_no iframe.b-iframe"))
        )
        driver.switch_to.frame(iframe)

        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@onclick, 'closeWin')]"))
        )
        driver.execute_script("arguments[0].click();", close_button)
        # iframe에서 메인 페이지로 돌아가기
        driver.switch_to.default_content()
        time.sleep(1)  # 버튼 클릭 후 잠시 대기

    except TimeoutException:
        print("모달 닫기 버튼이 존재하지 않음.")
        driver.switch_to.default_content()
    except Exception as e:
        print(f"모달 닫기 중 예외 발생: {e}")
        driver.switch_to.default_content()

    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()


    # 메인 창으로 전환
    driver.switch_to.window(main_window)

    # 공동주택(아파트, 다세대)일 경우
    # "표준단독주택공시가격"으로 이동
    link_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='공동주택공시가격']"))
        )
    link_element.click() 

    road_search = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='도로명검색']"))
    )
    road_search.click() 

    time.sleep(3)

    # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
    sido_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sido'))
    )
    select = Select(sido_list)
    select.select_by_visible_text(Sido)

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sigungu'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text(Sigungu)

    time.sleep(3)
    eub_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'initialword'))
    )
    select_2 = Select(eub_list)
    select_2.select_by_visible_text(Chosung)

    time.sleep(3)
    road_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'road'))
    )
    select_3 = Select(road_list)
    select_3.select_by_visible_text(Doro_Name)

    time.sleep(3)

    # 단지명 클릭
    apt = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'apt'))
    )
    select_4 = Select(apt)
    for option in select_4.options:
        if Building_Name in option.text:  # Building_Name이 포함된 텍스트를 찾음
            select_4.select_by_visible_text(option.text)
            break
    time.sleep(3)

    # 동 클릭
    dong = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'dong'))
    )
    select_4 = Select(dong)
    # Building_No1이 빈값인지 확인
    if not Building_No1 or Building_No1.strip() == "":
        print("Building_No1 값이 비어 있습니다. 동명없음 선택")
        select_4.select_by_index(0)  # 첫 번째 값 선택
    else:
        select_4.select_by_visible_text(Building_No1)  # Building_No1 값 선택
   
    # 호 클릭
    ho = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'ho'))
    )
    select_5 = Select(ho)
    select_5.select_by_visible_text(Room_No)

    time.sleep(3)

    # 열람하기 클릭
    show_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@class, 'btn-src3')]"))
    )
    driver.execute_script("goPage('1')", show_button)
    time.sleep(3)

    # 공동주택가격 값
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "opinNoticeAmt"))
    )
    
    # 값 추출 및 공백 제거
    raw_text = element.text.strip()
    print(f"Raw value: {raw_text}")  # 출력: '211,000,000'
    
    # 쉼표 제거 및 숫자로 변환
    realty_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {realty_value}")  # 출력: 211000000

    # 전용면적 값
    element_1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#dataList tr:first-child td:nth-child(5)"))
    )
    
    # 값 추출 및 공백 제거
    element_1_text = element_1.text.strip()
    print(f"element_1_text: {element_1_text}") 
    
    # 쉼표 제거 및 숫자로 변환
    area_value = float(element_1_text.replace(",", ""))
    print(f"area_value: {area_value}") 

    # 기준일 값
    date_element = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, "//tbody[@id='dataList']/tr[1]/td[1]"))
    )

    date_value = date_element.text

    return [realty_value, 0, area_value, date_value]


def realtyprice_individual_streetnum(driver, **kwargs):
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

    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    try:
        # 팝업 div이 포함된 iframe으로 전환
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#wrap_pop_no iframe.b-iframe"))
        )
        driver.switch_to.frame(iframe)

        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@onclick, 'closeWin')]"))
        )
        driver.execute_script("arguments[0].click();", close_button)
        # iframe에서 메인 페이지로 돌아가기
        driver.switch_to.default_content()
        time.sleep(1)  # 버튼 클릭 후 잠시 대기

    except TimeoutException:
        print("모달 닫기 버튼이 존재하지 않음.")
        driver.switch_to.default_content()
    except Exception as e:
        print(f"모달 닫기 중 예외 발생: {e}")
        driver.switch_to.default_content()

    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()


    # 메인 창으로 전환
    driver.switch_to.window(main_window)

    # "개별단독주택공시가격"으로 이동
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
    select.select_by_visible_text(Sido)

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sgg_list'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text(Sigungu)

    time.sleep(3)
    eub_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'eub_list'))
    )
    select_2 = Select(eub_list)
    select_2.select_by_visible_text(Ridong)

    time.sleep(3)
    
    # 번지 입력
    bun1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun1' and @class='text3']"))
    )
    driver.execute_script("arguments[0].click();", bun1)
    bun1.send_keys(Jibun_No1)

    time.sleep(3)
    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun2' and @class='text3']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys(Jibun_No2)

    time.sleep(3)
    # 검색 클릭            
    search_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@alt, '검색')]"))
    )
    driver.execute_script("goPage(1)", search_button)
    
    time.sleep(3)

    # XPath를 사용해 <tr> 태그 내부의 마지막 <td> 값(개별주택가격)을 가져옴
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//tr/td[last()]"))
    )
    
    # 텍스트 추출
    raw_text = element.text.strip()
    print(f"Raw value: {raw_text}")  # 예: '811,000,000'
    
    # 쉼표 제거 및 숫자로 변환
    realty_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {realty_value}")  # 예: 811000000
    
    # 대지면적(산정정)
    area_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//tbody[@id='dataList']/tr/td[4]"))
    )
    area_value = area_element.text.strip()

    # 기준일 값
    date_element = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, "//tbody[@id='dataList']/tr[1]/td[1]"))
    )

    date_value = date_element.text

    return [realty_value, 0, area_value, date_value]


def realtyprice_individual_roadnum(driver, **kwargs):
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

    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    try:
        # 팝업 div이 포함된 iframe으로 전환
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#wrap_pop_no iframe.b-iframe"))
        )
        driver.switch_to.frame(iframe)

        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@onclick, 'closeWin')]"))
        )
        driver.execute_script("arguments[0].click();", close_button)
        # iframe에서 메인 페이지로 돌아가기
        driver.switch_to.default_content()
        time.sleep(1)  # 버튼 클릭 후 잠시 대기

    except TimeoutException:
        print("모달 닫기 버튼이 존재하지 않음.")
        driver.switch_to.default_content()
    except Exception as e:
        print(f"모달 닫기 중 예외 발생: {e}")
        driver.switch_to.default_content()

    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()


    # 메인 창으로 전환
    driver.switch_to.window(main_window)

    time.sleep(3)

    # "개별단독주택공시가격"으로 이동
    link_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='개별단독주택공시가격']"))
    )
    link_element.click() 

    time.sleep(3)
    road_search = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='도로명검색']"))
    )
    road_search.click() 

    time.sleep(5)

    # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
    sido_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'area1'))
    )
    select = Select(sido_list)
    #select.select_by_index(1)
    select.select_by_visible_text(Sido)

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sigungu'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text(Sigungu)

    time.sleep(3)
    eub_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'initialword'))
    )
    select_2 = Select(eub_list)
    select_2.select_by_visible_text(Chosung)

    time.sleep(3)
    road_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'road'))
    )
    select_3 = Select(road_list)
    select_3.select_by_visible_text(Doro_Name)

    time.sleep(3)

    # 건물번호 입력
    bun1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun1' and @class='text3 input_number_only']"))
    )
    driver.execute_script("arguments[0].click();", bun1)
    bun1.send_keys(Building_No1)

    time.sleep(3)
    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun2' and @class='text3 input_number_only']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys(Building_No2)

    time.sleep(3)
    # 검색 클릭            
    search_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@alt, '검색')]"))
    )
    driver.execute_script("goPage(1)", search_button)
    
    time.sleep(3)

    # XPath를 사용해 <tr> 태그 내부의 마지막 <td> 값(개별주택가격)을 가져옴
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//tr/td[last()]"))
    )
    
    # 텍스트 추출
    raw_text = element.text.strip()
    print(f"Raw value: {raw_text}")  # 예: '811,000,000'
    
    # 쉼표 제거 및 숫자로 변환
    realty_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {realty_value}")  # 예: 811000000
    
    # 대지면적(산정정)
    area_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//tbody[@id='dataList']/tr/td[4]"))
    )
    area_value = area_element.text.strip()

    # 기준일 값
    date_element = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, "//tbody[@id='dataList']/tr[1]/td[1]"))
    )
    date_value = date_element.text

    return [realty_value, 0, area_value, date_value]


def realtyprice_land_streetnum(driver, **kwargs):
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

    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    try:
        # 팝업 div이 포함된 iframe으로 전환
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#wrap_pop_no iframe.b-iframe"))
        )
        driver.switch_to.frame(iframe)

        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@onclick, 'closeWin')]"))
        )
        driver.execute_script("arguments[0].click();", close_button)
        # iframe에서 메인 페이지로 돌아가기
        driver.switch_to.default_content()
        time.sleep(1)  # 버튼 클릭 후 잠시 대기

    except TimeoutException:
        print("모달 닫기 버튼이 존재하지 않음.")
        driver.switch_to.default_content()
    except Exception as e:
        print(f"모달 닫기 중 예외 발생: {e}")
        driver.switch_to.default_content()

    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()


    # 메인 창으로 전환
    driver.switch_to.window(main_window)

    # "표준단독주택공시가격"으로 이동
    link_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='개별공시지가']"))
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
    select.select_by_visible_text(Sido)

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sgg_list'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text(Sigungu)

    time.sleep(3)
    eub_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'eub_list'))
    )
    select_2 = Select(eub_list)
    select_2.select_by_visible_text(Ridong)

    time.sleep(3)

    # 지번 입력
    # 번지 입력
    bun1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun1' and @class='text3']"))
    )
    driver.execute_script("arguments[0].click();", bun1)
    bun1.send_keys(Jibun_No1)

    time.sleep(3)
    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun2' and @class='text3']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys(Jibun_No2)
    
    # '검색' 버튼 가져오기
    search_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='image' and @alt='검색']"))
    )

    # 버튼 클릭
    search_button.click()

    time.sleep(3)

    # XPath를 사용해 <tr> 태그 내부의 마지막 <td> 값(개별주택가격)을 가져옴
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//tr/td[4]"))
    )
    
    # 텍스트 값 가져오기
    raw_text = element.text.strip()  # '4,218,000 원/㎡' 형태
    print(f"Raw text: {raw_text}")
    
    # 쉼표와 단위 제거 및 숫자로 변환
    realty_land_value = int(raw_text.replace(",", "").split(" ")[0])  # 쉼표 제거 후 '원/㎡' 분리
    print(f"Numeric value: {realty_land_value}")  # 출력: 4218000
    
    return [realty_land_value, 0, 0, 0]

def realtyprice_land_roadnum(driver, **kwargs):
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

    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    try:
        # 팝업 div이 포함된 iframe으로 전환
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#wrap_pop_no iframe.b-iframe"))
        )
        driver.switch_to.frame(iframe)

        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@onclick, 'closeWin')]"))
        )
        driver.execute_script("arguments[0].click();", close_button)
        # iframe에서 메인 페이지로 돌아가기
        driver.switch_to.default_content()
        time.sleep(1)  # 버튼 클릭 후 잠시 대기

    except TimeoutException:
        print("모달 닫기 버튼이 존재하지 않음.")
        return None
    except Exception as e:
        print(f"모달 닫기 중 예외 발생: {e}")

    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()


    # 메인 창으로 전환
    driver.switch_to.window(main_window)

    # "표준단독주택공시가격"으로 이동
    link_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='개별공시지가']"))
    )
    link_element.click() 

    zibun_search = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='도로명검색']"))
    )
    zibun_search.click() 

    time.sleep(3)

    # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
    sido_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'area1'))
    )
    select = Select(sido_list)
    select.select_by_visible_text(Sido)

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sigungu'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text(Sigungu)

    time.sleep(3)
    initialword = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'initialword'))
    )
    select_2 = Select(initialword)
    select_2.select_by_visible_text(Chosung)

    time.sleep(3)
    road = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'road'))
    )
    select_3 = Select(road)
    select_3.select_by_visible_text(Doro_Name)

    time.sleep(3)

    # 건물번호
    bun1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun1' and @class='text3 input_number_only']"))
    )
    driver.execute_script("arguments[0].click();", bun1)
    bun1.send_keys(Building_No1)

    time.sleep(3)
    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun2' and @class='text3 input_number_only']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys(Building_No2)
    
    # '검색' 버튼 가져오기
    search_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='image' and @alt='검색']"))
    )

    # 버튼 클릭
    search_button.click()

    time.sleep(3)

    # XPath를 사용해 <tr> 태그 내부의 마지막 <td> 값(개별주택가격)을 가져옴
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//tr/td[4]"))
    )
    
    # 텍스트 값 가져오기
    raw_text = element.text.strip()  # '4,218,000 원/㎡' 형태
    print(f"Raw text: {raw_text}")
    
    # 쉼표와 단위 제거 및 숫자로 변환
    realty_land_value = int(raw_text.replace(",", "").split(" ")[0])  # 쉼표 제거 후 '원/㎡' 분리
    print(f"Numeric value: {realty_land_value}")  # 출력: 4218000
    
    return [realty_land_value, 0, 0, 0]

