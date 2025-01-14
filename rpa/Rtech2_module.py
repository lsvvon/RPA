import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
from io import BytesIO
import predict_sh
from PIL import Image
from selenium.common.exceptions import TimeoutException

def rtech_app_streetnum(driver, **kwargs):
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

    url = "https://www.rtech.or.kr/main/mapSearch_mp.do?popUpYn=&posX=37.48243936583027&posY=127.06183029780048#"
    driver.get(url)
    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()

    close_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//area[@alt='닫기']"))
    )
    close_button.click()

    
    # 1. 시도 선택
    select = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'do_code1'))
    )
    select = Select(select)
    select.select_by_visible_text(Sido)

    # 2. 시군구 선택
    select_1 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'city_code1'))
    )
    select_1 = Select(select_1)
    select_1.select_by_visible_text(Sigungu)

    # 3. 읍면동 선택
    select_2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'dong_code1'))
    )
    select_2 = Select(select_2)
    select_2.select_by_visible_text(Ridong)

    # 4. 빠른검색 입력
    search_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "searchInput"))
    )
    building_name = Building_Name
    search_address = Sido + " " + Sigungu
    search_input.send_keys(building_name)

    time.sleep(3)
    # 2. 검색 결과 리스트 확인
    results_ul = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "quickSearchResult"))
    )
    result_items = results_ul.find_elements(By.TAG_NAME, "li")  # 검색 결과 리스트의 각 항목
    
    time.sleep(3)
    # "검색 결과가 없습니다." 
    for item in result_items:
        if "검색 결과가 없습니다." in item.text:
            print("검색 결과가 없습니다. 프로그램을 종료합니다.")
            return None  # 종료
    time.sleep(3)

    # 완전 일치하는 항목 찾기
    matching_item = None
    search_keywords = search_address.split() 

    for item in result_items:
        item_text = item.text.replace(" ", "")  # 공백 제거 후 비교
        # 각 검색어가 항목에 포함되는지 확인
        if all(keyword in item_text for keyword in search_keywords) and building_name in item_text:
            matching_item = item
            break

    time.sleep(5)
    if matching_item:
        print(f"일치하는 주소 '{search_address}'를 찾았습니다. 클릭합니다.")
        driver.execute_script("arguments[0].scrollIntoView(true);", matching_item)
        matching_item.click()
    else:
        print(f"주소 '{search_address}'에 대한 일치 결과를 찾을 수 없습니다. 프로그램을 종료합니다.")
        return None
    
    time.sleep(3)
    # 3. 해당 아파트 항목 클릭
    building_name = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "map_pop_infobox_tit1"))
    )
    time.sleep(3)
    apt_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//ul[@id='aptListArea']//li/a[contains(text(), '{building_name.text}')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
    apt_element.click()


def rtech_app_roadnum(driver, **kwargs):
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

    url = "https://www.rtech.or.kr/main/mapSearch_mp.do?popUpYn=&posX=37.48243936583027&posY=127.06183029780048#"
    driver.get(url)
    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()
    
    close_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//area[@alt='닫기']"))
    )
    close_button.click()

    # 4. 빠른검색 입력
    search_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "searchInput"))
    )
    search_address = Doro_Name
    search_input.send_keys(search_address)

    time.sleep(3)
    # 검색 결과 리스트 확인
    results_ul = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "quickSearchResult"))
    )
    result_items = results_ul.find_elements(By.TAG_NAME, "li")  # 검색 결과 리스트의 각 항목
    
    time.sleep(3)
    # "검색 결과가 없습니다." 
    for item in result_items:
        if "검색 결과가 없습니다." in item.text:
            print("검색 결과가 없습니다. 프로그램을 종료합니다.")
            return None  # 종료
    time.sleep(3)

    # 완전 일치하는 항목 찾기
    matching_item = None
    search_keywords = search_address.split() 

    for item in result_items:
        item_text = item.text.replace(" ", "")  # 공백 제거 후 비교
        # 각 검색어가 항목에 포함되는지 확인
        if all(keyword in item_text for keyword in search_keywords):
            matching_item = item
            break

    time.sleep(5)
    if matching_item:
        print(f"일치하는 주소 '{search_address}'를 찾았습니다. 클릭합니다.")
        driver.execute_script("arguments[0].scrollIntoView(true);", matching_item)
        matching_item.click()
    else:
        print(f"주소 '{search_address}'에 대한 일치 결과를 찾을 수 없습니다. 프로그램을 종료합니다.")
        return None
    
    time.sleep(3)
    # 3. 해당 아파트 항목 클릭
    building_name = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "map_pop_infobox_tit1"))
    )
    time.sleep(3)
    apt_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//ul[@id='aptListArea']//li/a[contains(text(), '{building_name.text}')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
    apt_element.click()

def captcha_APP(driver, **kwargs):
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

    # 팝업창 확인 후 처리
    if len(driver.window_handles) > 1:
        print("팝업창이 감지되었습니다. 팝업창으로 전환합니다.")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
    else:
        print("팝업창이 감지되지 않았습니다. 현재 화면에서 캡처를 진행합니다.")
        return None

    time.sleep(3)

    # 8. 팝업 내 '호별 시세조회' 요소 클릭
    ho_background = WebDriverWait(driver, 20).until(
        # EC.visibility_of_element_located((By.XPATH, '//span[text()="호별 시세조회"]'))
        EC.presence_of_element_located((By.ID, "DongHoInfo"))
    )
    driver.execute_script("javascript:infotabChange(2);", ho_background)

    time.sleep(3)
    # 9. 동, 호수 선택
    # 동
    select_dong = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'dong_'))
    )
    select_dong = Select(select_dong)
    # Building_No1이 빈값인지 확인
    if not Building_No1 or Building_No1.strip() == "":
        print("Building_No1 값이 비어 있습니다. 동명없음 선택")
        select_dong.select_by_visible_text("동명없음")   # 첫 번째 값 선택
    else:
        select_dong.select_by_visible_text(Building_No1) 

    time.sleep(2)
    # 호
    select_ho_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'ho_code'))
    )
    select_ho = Select(select_ho_element)
    select_ho.select_by_visible_text(Room_No)
    time.sleep(2)

    # 10. 보안문자 (캡차 이미지 다운로드)
    # 보안문자 (캡차 이미지 다운로드 스크린샷 방식)
    # 전체 페이지의 사이즈를 구하여 브라우저의 창 크기를 확대하고 스크린캡처를 합니다.

    save_path = r"C:\python\RPA\rpa\captcha_images_save"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    page_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    page_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(page_width, page_height)
    png = driver.get_screenshot_as_png()
    
    captcha_img = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "captchaImg"))
    )

    element = captcha_img
    image_location = element.location
    image_size = element.size
    
    # 이미지를 element의 위치에 맞춰서 crop 하고 저장합니다.
    im = Image.open(BytesIO(png))
    left = image_location['x']
    top = image_location['y']
    right = image_location['x'] + image_size['width']
    bottom = image_location['y'] + image_size['height']
    im = im.crop((left, top, right, bottom))

    captcha_filename = os.path.join(save_path, "capcha.png")
    im.save(captcha_filename)

    captcha_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "capcha"))
    )
    time.sleep(5)

    captcha_input.send_keys(predict_sh.get_predictions())

    # 확인버튼 클릭
    confirm_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@onclick='javascript:search_dongho_price()']"))
    )
    confirm_button.click()
    time.sleep(5)

    # 캡챠 틀렸을 경우 다시 새로고침 후 시도
    # while True:
    #     try:
    #         alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    #         if alert:
    #             print("캡차 오류 발생. 새로고침합니다.")
    #             alert.accept()
    #             button = WebDriverWait(driver, 20).until(
    #                 EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='javascript:captchaReload()']"))
    #             )
    #             button.click()

    #             # 새로고침 후 새로운 캡차 이미지가 로드될 때까지 대기
    #             time.sleep(5)
                
    #             # 캡차 이미지 다운로드 및 입력 재시도
    #             png = driver.get_screenshot_as_png()
    #             im = Image.open(BytesIO(png))
    #             im.save(captcha_filename)

    #             captcha_input = WebDriverWait(driver, 20).until(
    #                 EC.element_to_be_clickable((By.ID, "capcha"))
    #             )
    #             captcha_input.clear()
    #             captcha_input.send_keys(predict_sh.get_predictions())

    #             # 확인버튼 클릭
    #             confirm_button = WebDriverWait(driver, 20).until(
    #                 EC.element_to_be_clickable((By.XPATH, "//button[@onclick='javascript:search_dongho_price()']"))
    #             )
    #             confirm_button.click()
    #             time.sleep(5)
    #     except TimeoutException:
    #         print("Alert did not appear. 캡차가 맞았거나 다른 문제가 발생했습니다.")
    #         break


    # 하한평균가
    element_low = WebDriverWait(drjjiver, 20).until(
        EC.visibility_of_element_located((By.ID, "lower_trade_amt"))
    )
    # 텍스트 값 가져오기
    raw_element_low = element_low.text.strip()
    print(f"Raw text: {raw_element_low}")
    # 쉼표 제거 및 숫자로 변환
    rtechApp_low_value = int(raw_element_low.replace(",", ""))
    print(f"Numeric value: {rtechApp_low_value}")


    return [0, rtechApp_low_value, 0]
    
   