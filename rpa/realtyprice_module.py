from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support.select import Select


# 공동주택(아파트, 다세대)일 경우 - 지번 검색
def realtyprice_apt_streetnum(driver):
    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

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
    bun1.send_keys("149")

    time.sleep(3)
    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun2' and @class='text2']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys("9")

    time.sleep(3)
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
    select_3.select_by_visible_text("(149-9) 네이처하우스")

    time.sleep(3)
    # 동 클릭
    dong = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'dong'))
    )
    select_4 = Select(dong)
    select_4.select_by_visible_text("1")

    time.sleep(3)
    # 호 클릭
    ho = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'ho'))
    )
    select_5 = Select(ho)
    select_5.select_by_visible_text("302")

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
    numeric_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {numeric_value}")  # 출력: 211000000
    return numeric_value

def realtyprice_apt_roadnum(driver):
    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

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
    select.select_by_visible_text("서울특별시")

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sigungu'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text("송파구")

    time.sleep(3)
    eub_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'initialword'))
    )
    select_2 = Select(eub_list)
    select_2.select_by_visible_text("ㄷ")

    time.sleep(3)
    road_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'road'))
    )
    select_3 = Select(road_list)
    select_3.select_by_visible_text("도곡로62길")

    time.sleep(3)

    # 단지명 클릭
    apt = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'apt'))
    )
    select_4 = Select(apt)
    select_4.select_by_visible_text("(304-2) 쉐르빌(304-2)")
    time.sleep(3)

    # 동 클릭
    dong = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'dong'))
    )
    select_4 = Select(dong)
    select_4.select_by_visible_text("동명없음")

    time.sleep(3)
    # 호 클릭
    ho = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'ho'))
    )
    select_5 = Select(ho)
    select_5.select_by_visible_text("201")

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
    numeric_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {numeric_value}")  # 출력: 211000000

    return numeric_value 


def realtyprice_individual_streetnum(driver):
    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

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
    select.select_by_visible_text("서울특별시")

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sgg_list'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text("용산구")

    time.sleep(3)
    eub_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'eub_list'))
    )
    select_2 = Select(eub_list)
    select_2.select_by_visible_text("용문동")

    time.sleep(3)
    
    # 번지 입력
    bun1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun1' and @class='text3']"))
    )
    driver.execute_script("arguments[0].click();", bun1)
    bun1.send_keys("38")

    time.sleep(3)
    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun2' and @class='text3']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys("65")

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
    numeric_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {numeric_value}")  # 예: 811000000
    
    return numeric_value 


def realtyprice_individual_roadnum(driver):
    url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
    driver.get(url)

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

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
    select.select_by_visible_text("서울특별시")

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sigungu'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text("송파구")

    time.sleep(3)
    eub_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'initialword'))
    )
    select_2 = Select(eub_list)
    select_2.select_by_visible_text("ㄷ")

    time.sleep(3)
    road_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'road'))
    )
    select_3 = Select(road_list)
    select_3.select_by_visible_text("도곡로62길")

    time.sleep(3)

    # 건물번호 입력
    bun1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun1' and @class='text3 input_number_only']"))
    )
    driver.execute_script("arguments[0].click();", bun1)
    bun1.send_keys("15")

    time.sleep(3)
    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun2' and @class='text3 input_number_only']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys("11")

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
    numeric_value = int(raw_text.replace(",", ""))
    print(f"Numeric value: {numeric_value}")  # 예: 811000000
    
    return numeric_value

def realtyprice_land_streetnum(driver):
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
    select.select_by_visible_text("서울특별시")

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sgg_list'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text("중랑구")

    time.sleep(3)
    eub_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'eub_list'))
    )
    select_2 = Select(eub_list)
    select_2.select_by_visible_text("신내동")

    time.sleep(3)

    # 지번 입력
    # 번지 입력
    bun1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun1' and @class='text3']"))
    )
    driver.execute_script("arguments[0].click();", bun1)
    bun1.send_keys("835")

    time.sleep(3)
    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='bun2' and @class='text3']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys("")
    
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
    numeric_value = int(raw_text.replace(",", "").split(" ")[0])  # 쉼표 제거 후 '원/㎡' 분리
    print(f"Numeric value: {numeric_value}")  # 출력: 4218000
    
    # 등기부 상 대지권 비율과 곱하여 산정
    return numeric_value

def realtyprice_land_roadnum(driver):
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
    select.select_by_visible_text("서울특별시")

    time.sleep(3)
    sgg_list = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'sigungu'))
    )
    select_1 = Select(sgg_list)
    select_1.select_by_visible_text("중랑구")

    time.sleep(3)
    initialword = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'initialword'))
    )
    select_2 = Select(initialword)
    select_2.select_by_visible_text("ㄱ")

    time.sleep(3)
    road = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'road'))
    )
    select_3 = Select(road)
    select_3.select_by_visible_text("겸재로10가길")

    time.sleep(3)

    # 건물번호
    bun1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun1' and @class='text3 input_number_only']"))
    )
    driver.execute_script("arguments[0].click();", bun1)
    bun1.send_keys("12")

    time.sleep(3)
    bun2 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun2' and @class='text3 input_number_only']"))
    )
    driver.execute_script("arguments[0].click();", bun2)
    bun2.send_keys("")
    
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
    numeric_value = int(raw_text.replace(",", "").split(" ")[0])  # 쉼표 제거 후 '원/㎡' 분리
    print(f"Numeric value: {numeric_value}")  # 출력: 4218000
    
    # 등기부 상 대지권 비율과 곱하여 산정
    return numeric_value

