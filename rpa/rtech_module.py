import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import os
from io import BytesIO
import predict_sh
from PIL import Image

# SSL 인증서 검증 무시 설정
# ssl._create_default_https_context = ssl._create_unverified_context

def rtech_streetnum(driver): 
    url = "https://rtech.or.kr/main/mapSearch.do?posX="
    driver.get(url)
    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()

    # 1. 시도 선택
    select = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'do_code1'))
    )
    select = Select(select)
    select.select_by_visible_text("서울특별시")

    # 2. 시군구 선택
    select_1 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'city_code1'))
    )
    select_1 = Select(select_1)
    select_1.select_by_visible_text("중랑구")

    # 3. 읍면동 선택
    select_2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'dong_code1'))
    )
    select_2 = Select(select_2)
    select_2.select_by_visible_text("상봉동")

    # 4. 빠른검색 입력
    search_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "searchInput"))
    )
    search_input.send_keys("상봉동 동부아파트")

    # 5. 검색 결과 클릭
    quick_search_result = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "quickSearchResult"))
    )
    quick_search_result.click()
    time.sleep(3)

    apt_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//ul[@id='aptListArea']//li/a[contains(text(), '동부아파트')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
    apt_element.click()

def rtech_roadnum(driver): 
    url = "https://rtech.or.kr/main/mapSearch.do?posX="
    driver.get(url)
    # 현재 창 정보
    main_window = driver.current_window_handle

    # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
    for window in driver.window_handles:
        if window != main_window:
            driver.switch_to.window(window)
            driver.close()

    # 1. 빠른검색 입력
    search_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "searchInput"))
    )
    search_input.send_keys("고덕로 333")

    # 2. 검색 결과 클릭
    quick_search_result = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "quickSearchResult"))
    )
    quick_search_result.click()

    apt_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//ul[@id='aptListArea']//li/a[contains(text(), '고덕그라시움')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
    apt_element.click()



def captcha(driver):
    # 7. 팝업창으로 창 전환
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
    # 8. 팝업 내 '호별 시세조회' 요소 클릭
    ho_background = WebDriverWait(driver, 20).until(
        # EC.visibility_of_element_located((By.XPATH, '//span[text()="호별 시세조회"]'))
        EC.presence_of_element_located((By.ID, "DongHoInfo"))
    )
    driver.execute_script("javascript:infotabChange(2);", ho_background)

    # 9. 동, 호수 선택
    select_dong = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'dong_'))
    )
    select_dong = Select(select_dong)
    #select_dong.select_by_visible_text("101")
    select_dong.select_by_index(1)
    time.sleep(2)
    select_ho_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'ho_code'))
    )
    select_ho = Select(select_ho_element)
    select_ho.select_by_index(2)
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

def rtech_app_streetnum(driver):
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
    select.select_by_visible_text("서울특별시")

    # 2. 시군구 선택
    select_1 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'city_code1'))
    )
    select_1 = Select(select_1)
    select_1.select_by_visible_text("강남구")

    # 3. 읍면동 선택
    select_2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'dong_code1'))
    )
    select_2 = Select(select_2)
    select_2.select_by_visible_text("개포동")

    # 4. 빠른검색 입력
    search_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "searchInput"))
    )
    search_input.send_keys("개포자이르네")
    time.sleep(3)

    # 5. 검색 결과 클릭
    quick_search_result = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "quickSearchResult"))
    )
    quick_search_result.click()
    time.sleep(3)

    apt_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//ul[@id='aptListArea']//li/a[contains(text(), '개포자이르네')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
    apt_element.click()

def rtech_app_roadnum(driver):
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

    # 1. 빠른검색 입력
    search_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "searchInput"))
    )
    search_input.send_keys("고덕로 10길 30")

    # 2. 검색 결과 클릭
    quick_search_result = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "quickSearchResult"))
    )
    quick_search_result.click()

    apt_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//ul[@id='aptListArea']//li/a[contains(text(), '우암쎈스뷰')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
    apt_element.click()
