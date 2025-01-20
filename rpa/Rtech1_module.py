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

# SSL 인증서 검증 무시 설정
# ssl._create_default_https_context = ssl._create_unverified_context

def rtech_streetnum(driver, Estate_Gubun, **kwargs): 
    response = {
        "response_code": None,
        "response_msg": None,
        "data": None,
    }

    if Estate_Gubun == '1':
        Estate_Name = '아파트'
        Estate_ch = '아'
    elif Estate_Gubun == '4':
        Estate_Name = '오피스텔'
        Estate_ch = '오'

    try:
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


        url = "https://rtech.or.kr/main/mapSearch.do?posX="
        driver.get(url)
        # 현재 창 정보
        main_window = driver.current_window_handle

        # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
        for window in driver.window_handles:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()

        time.sleep(5)

        try:
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
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 선택 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response

        try:
            # 4. 빠른검색 입력(건물이름)
            search_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "searchInput"))
            )
            building_name = Building_Name
            search_address = Sido + " " + Sigungu + " " + Ridong
            search_input.send_keys(building_name)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 입력 필드를 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)

        try:
            # 2. 검색 결과 리스트 확인
            results_ul = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "quickSearchResult"))
            )
            result_items = results_ul.find_elements(By.TAG_NAME, "li")  # 검색 결과 리스트의 각 항목
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 결과 리스트를 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response            
        time.sleep(3)

        try:
            # "검색 결과가 없습니다." 
            for item in result_items:
                if "검색 결과가 없습니다." in item.text:
                    response["response_code"] = "90000001"
                    response["response_msg"] = "검색 결과가 없습니다. 프로그램을 종료합니다."
                    response["data"] = [0, 0, 0, 0]
                    return response
        except Exception as e:
            response["response_code"] = "90000001"
            response["response_msg"] = f"검색 결과 처리 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)
        # 완전 일치하는 항목 찾기
        try:
            matching_item = None
            search_keywords = search_address.split() 

            for item in result_items:
                item_text = item.text.replace(" ", "")  # 공백 제거 후 비교
                # 각 검색어가 항목에 포함되는지 확인
                if all(keyword in item_text for keyword in search_keywords) and building_name in item_text and Estate_Name in item_text:
                    matching_item = item
                    break

            time.sleep(5)
            if matching_item:
                driver.execute_script("arguments[0].scrollIntoView(true);", matching_item)
                matching_item.click()
            else:
                response["response_code"] = "90000001"
                response["response_msg"] = f"주소 '{search_address}'에 대한 일치 결과를 찾을 수 없습니다. 프로그램을 종료합니다."
                response["data"] = [0, 0, 0, 0]
                return response
            
        except Exception as e:
            response["response_code"] = "90000001"
            response["response_msg"] = f"항목 선택 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response        
        time.sleep(3)

        try:
            # 3. 해당 아파트 항목 클릭
            building_name = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "map_pop_infobox_tit1"))
            )
            time.sleep(3)
            apt_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[contains(@href, 'go_apt_info') and contains(., '{Estate_ch}') and contains(., '{building_name.text}')]")
            )
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
            apt_element.click()
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "물건지 항목 클릭 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            response["response_code"] = "90000001"
            response["response_msg"] = f"물건지 항목 클릭 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
                
    except Exception as e:
        response["response_code"] = "90000001"
        response["response_msg"] = f"프로세스 실행 중 알 수 없는 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    return response


def rtech_roadnum(driver, Estate_Gubun, **kwargs): 
    response = {
        "response_code": None,
        "response_msg": None,
        "data": None,
    }

    if Estate_Gubun == '1':
        Estate_Name = '아파트'
        Estate_ch = '아'
    elif Estate_Gubun == '4':
        Estate_Name = '오피스텔'
        Estate_ch = '오'


    try:
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

        url = "https://rtech.or.kr/main/mapSearch.do?posX="
        driver.get(url)
        # 현재 창 정보
        main_window = driver.current_window_handle

        # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
        for window in driver.window_handles:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()

        try:
            # 1. 빠른검색 입력
            search_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "searchInput"))
            )
            search_address = Doro_Name
            search_input.send_keys(search_address)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 입력 필드를 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)
        
        try:
            # 2. 검색 결과 리스트 확인
            results_ul = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "quickSearchResult"))
            )
            result_items = results_ul.find_elements(By.TAG_NAME, "li")  # 검색 결과 리스트의 각 항목
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 결과 리스트를 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response            
        time.sleep(3)

        try:
            # "검색 결과가 없습니다." 
            for item in result_items:
                if "검색 결과가 없습니다." in item.text:
                    response["response_code"] = "90000001"
                    response["response_msg"] = "검색 결과가 없습니다. 프로그램을 종료합니다."
                    response["data"] = [0, 0, 0, 0]
                    return response
        except Exception as e:
            response["response_code"] = "90000001"
            response["response_msg"] = f"검색 결과 처리 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)
        # 완전 일치하는 항목 찾기
        matching_item = None
        search_keywords = search_address.split() 

        try:
            for item in result_items:
                item_text = item.text.replace(" ", "")  # 공백 제거 후 비교
                # 각 검색어가 항목에 포함되는지 확인
                if all(keyword in item_text for keyword in search_keywords):
                    matching_item = item
                    break
            time.sleep(5)
            if matching_item:
                driver.execute_script("arguments[0].scrollIntoView(true);", matching_item)
                matching_item.click()
            else:
                response["response_code"] = "90000001"
                response["response_msg"] = f"주소 '{search_address}'에 대한 일치 결과를 찾을 수 없습니다. 프로그램을 종료합니다."
                response["data"] = [0, 0, 0, 0]
                return response
        except Exception as e:
            response["response_code"] = "90000001"
            response["response_msg"] = f"검색 결과 처리 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        
        time.sleep(3)

        try: 
            # 3. 해당 아파트 항목 클릭
            building_name = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "map_pop_infobox_tit1"))
            )
            
            apt_element = WebDriverWait(driver, 20).until(
                #EC.element_to_be_clickable((By.XPATH, f"//ul[@id='aptListArea']//li/a[contains(text(), '{building_name.text}')]"))
                (By.XPATH, f"//a[contains(@href, 'go_apt_info') and contains(., '{Estate_ch}') and contains(., '{building_name.text}')]")
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
            apt_element.click()
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "물건지 항목 클릭 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            response["response_code"] = "90000001"
            response["response_msg"] = f"물건지 항목 클릭 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
                
    except Exception as e:
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response

    return response

def captcha_HUG(driver, Estate_Gubun, **kwargs):
    response = {
        "response_code": None,
        "response_msg": None,
        "data": None,
    }
    try:
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

        try:
            # 8. 팝업 내 '호별 시세조회' 요소 클릭
            ho_background = WebDriverWait(driver, 20).until(

                EC.presence_of_element_located((By.ID, "DongHoInfo"))
            )
            driver.execute_script("javascript:infotabChange(2);", ho_background)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "호별 시세조회 요소를 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            response["response_code"] = "90000001"
            response["response_msg"] = f"호별 시세조회 클릭 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response

        # 물건지 정보가 아파트일 경우
        if Estate_Gubun == '1':
            try:
                # 9. 동, 호수 선택
                select_dong = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, 'dong_'))
                )
                select_dong = Select(select_dong)
                select_dong.select_by_visible_text(Building_No1)
            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"동 선택 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
            time.sleep(2)
            try:
                select_ho_element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, 'ho_code'))
                )
                select_ho = Select(select_ho_element)
                select_ho.select_by_visible_text(Room_No)
            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"호 선택 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
            time.sleep(2)
            # 10. 보안문자 (캡차 이미지 다운로드)
            # 보안문자 (캡차 이미지 다운로드 스크린샷 방식)
            # 전체 페이지의 사이즈를 구하여 브라우저의 창 크기를 확대하고 스크린캡처를 합니다.

            try:
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
            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"캡차 이미지 처리 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
            # 캡차 입력
            try:
                captcha_input = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "capcha"))
                )
                time.sleep(5)

                captcha_input.send_keys(predict_sh.get_predictions())
            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"캡차 입력 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
            # 확인 버튼 클릭
            try:
                confirm_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@onclick='javascript:search_dongho_price()']"))
                )
                confirm_button.click()
            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"확인 버튼 클릭 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
            time.sleep(5)
            
            # 호별시세 안나오는 경우, 면적별 시세 조회
            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                if alert:
                    alert.accept()
                    size_background = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "pyongMarketPriceTitle"))
                    )
                    driver.execute_script("javascript:infotabChange(1);", size_background)
                    try:
                        # 하한평균가
                        element_low = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "//td[@class='table_txt_blue'][1]"))
                        )
                        # 상향평균가
                        element_high = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "//td[@class='table_txt_red'][1]"))
                        )
                        # 텍스트 값 가져오기
                        raw_element_low = element_low.text.strip()
                        raw_element_high = element_high.text.strip()

                        # 쉼표 제거 및 숫자로 변환
                        rtech_low_value = int(raw_element_low.replace(",", ""))
                        rtech_high_value = int(raw_element_high.replace(",", ""))
                        response["response_code"] = "00000000"
                        response["response_msg"] = "성공적으로 상한/하한평균가를 가져왔습니다."
                        response["data"] = [rtech_high_value, rtech_low_value, 0]
                    
                    except Exception as e:
                        response["response_code"] = "90000001"
                        response["response_msg"] = f"상한/하한평균가 가져오기 중 예외 발생: {e}"
                        response["data"] = [0, 0, 0, 0]
                        return response
                    
            except TimeoutException:
                response["response_code"] = "90000000"
                response["response_msg"] = f"면적별 시세 조회 중 예외 발생"
                response["data"] = [0, 0, 0, 0]

            try:
                # 하한평균가
                element_low = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.ID, "lower_trade_amt"))
                )
                # 상향평균가
                element_high = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.ID, "upper_trade_amt"))
                )
                # 텍스트 값 가져오기
                raw_element_low = element_low.text.strip()
                raw_element_high = element_high.text.strip()

                # 쉼표 제거 및 숫자로 변환
                rtech_low_value = int(raw_element_low.replace(",", ""))
                rtech_high_value = int(raw_element_high.replace(",", ""))
                response["response_code"] = "00000000"
                response["response_msg"] = "성공적으로 상한/하한평균가를 가져왔습니다."
                response["data"] = [rtech_high_value, rtech_low_value, 0]

            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"상한/하한평균가 가져오기 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
        # 물건지 정보가 오피스텔일 경우
        elif Estate_Gubun == '4':
            try:
                select_ho_element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, 'office_ho_code'))
                )
                select_ho = Select(select_ho_element)
                select_ho.select_by_visible_text(Room_No)
                time.sleep(2)
            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"호 선택 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
            
            # 캡차 이미지 처리
            try:
                save_path = r"C:\python\RPA\rpa\captcha_images_save"
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                page_width = driver.execute_script('return document.body.parentNode.scrollWidth')
                page_height = driver.execute_script('return document.body.parentNode.scrollHeight')
                driver.set_window_size(page_width, page_height)
                png = driver.get_screenshot_as_png()
                
                captcha_img = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "office_captchaImg"))
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
            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"캡차 이미지 처리 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
            
            # 캡챠 입력
            try:
                captcha_input = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "office_capcha"))
                )
                time.sleep(5)

                captcha_input.send_keys(predict_sh.get_predictions())
            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"캡차 입력 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response

            # 확인버튼 클릭
            try:
                confirm_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@onclick='javascript:office_search_dongho_price()']"))
                )
                confirm_button.click()
            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"확인 버튼 클릭 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response

            time.sleep(5)

            # 호별시세 안나오는 경우, 면적별 시세 조회
            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                if alert:
                    alert.accept()
                    size_background = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "pyongMarketPriceTitle"))
                    )
                    driver.execute_script("javascript:infotabChange(1);", size_background)
                    try:
                        # 하한평균가
                        element_low = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "//td[@class='table_txt_blue'][1]"))
                        )
                        # 상향평균가
                        element_high = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "//td[@class='table_txt_red'][1]"))
                        )
                        
                        # 텍스트 값 가져오기
                        raw_element_low = element_low.text.strip()
                        raw_element_high = element_high.text.strip()

                        # 쉼표 제거 및 숫자로 변환
                        rtech_low_value = int(raw_element_low.replace(",", ""))
                        rtech_high_value = int(raw_element_high.replace(",", ""))
                        response["response_code"] = "00000000"
                        response["response_msg"] = "성공적으로 하한평균가를 가져왔습니다."
                        response["data"] = [0, rtech_low_value, 0, 0]
                    except Exception as e:
                        response["response_code"] = "90000001"
                        response["response_msg"] = f"상한/하한평균가 가져오기 중 예외 발생: {e}"
                        response["data"] = [0, 0, 0, 0]
                        return response
                    
            except TimeoutException:
                response["response_code"] = "90000000"
                response["response_msg"] = f"면적별 시세 조회 중 예외 발생"
                response["data"] = [0, 0, 0, 0]

            time.sleep(5)

            try:
                # 하한평균가
                element_low = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.ID, "office_lower_trade_amt"))
                )
                # 텍스트 값 가져오기
                raw_element_low = element_low.text.strip()
                print(f"Raw text: {raw_element_low}")

                # 쉼표 제거 및 숫자로 변환
                rtech_low_value = int(raw_element_low.replace(",", ""))
                print(f"Numeric value: {rtech_low_value}")
                response["response_code"] = "00000000"
                response["response_msg"] = "성공적으로 하한평균가를 가져왔습니다."
                response["data"] = [0, rtech_low_value, 0, 0]

            except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"하한평균가 가져오기 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
    except Exception as e:
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response

    return response


def search_HF(driver):
    response = {
        "response_code": None,
        "response_msg": None,
        "data": None
    }
    try:
        # 팝업창 확인 후 처리
        if len(driver.window_handles) > 1:
            print("팝업창이 감지되었습니다. 팝업창으로 전환합니다.")
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)
        else:
            print("팝업창이 감지되지 않았습니다. 현재 화면에서 캡처를 진행합니다.")
            return None
        
        time.sleep(3)

        try:
            # 하한평균가
            element_low = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//tr/td[3]"))
            )
            # 상향평균가
            element_high = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//tr/td[4]"))
            )
            
            # 텍스트 값 가져오기
            raw_element_low = element_low.text.strip()
            raw_element_high = element_high.text.strip()

            # 쉼표 제거 및 숫자로 변환
            rtech_low_value = int(raw_element_low.replace(",", ""))
            rtech_high_value = int(raw_element_high.replace(",", ""))
            response["response_code"] = "00000000"
            response["response_msg"] = "성공적으로 하한평균가를 가져왔습니다."
            response["data"] = [rtech_high_value, rtech_low_value, 0, 0]
            
        except Exception as e:
                response["response_code"] = "90000001"
                response["response_msg"] = f"상한/하한평균가 가져오기 중 예외 발생: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
        
    except Exception as e:
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response

    return response
