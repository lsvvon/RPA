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

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementClickInterceptedException, WebDriverException
)
import time

def rtech_app_streetnum(driver, kwargs):
    response = {
        "response_code": None,
        "response_msg": None,
        "data": None,
    }
    
    try:
        # 주소 값 가져오기
        Sido = kwargs.get('Sido1')
        Sigungu = kwargs.get('Sigungu1')
        Sigungu2 = kwargs.get('Sigungu2')
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

        # 팝업 창 닫기
        try:
            for window in driver.window_handles:
                if window != main_window:
                    driver.switch_to.window(window)
                    driver.close()
            driver.switch_to.window(main_window)
        except WebDriverException as e:
            response["response_code"] = "90000000"
            response["response_msg"] = f"팝업 창 닫기 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response

        try:
            close_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//area[@alt='닫기']"))
            )
            close_button.click()
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "팝업 닫기 버튼을 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response
        except ElementClickInterceptedException:
            response["response_code"] = "90000001"
            response["response_msg"] = "팝업 닫기 버튼 클릭이 차단되었습니다."
            response["data"] = [0, 0, 0, 0]
            return response

        # 1. 시도 선택
        try:
            select = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, 'do_code1'))
            )
            select = Select(select)
            select.select_by_visible_text(Sido)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "시도 선택 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response

        # 2. 시군구 선택
        try:
            select_1 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, 'city_code1'))
            )
            select_1 = Select(select_1)
            select_1.select_by_visible_text(Sigungu2)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "시군구 선택 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response

        # 3. 읍면동 선택
        try:
            select_2 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, 'dong_code1'))
            )
            select_2 = Select(select_2)
            select_2.select_by_visible_text(Ridong)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "읍면동 선택 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response

        # 4. 빠른검색 입력
        try:
            search_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "searchInput"))
            )
            building_name = Building_Name
            search_address = Sido + " " + Sigungu2
            search_input.send_keys(building_name)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 입력 필드를 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(3)

        # 5. 검색 결과 리스트 확인
        try:
            results_ul = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "quickSearchResult"))
            )
            result_items = results_ul.find_elements(By.TAG_NAME, "li")
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 결과 리스트를 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(3)

        # "검색 결과가 없습니다."
        try:
            for item in result_items:
                if "검색 결과가 없습니다." in item.text:
                    response["response_code"] = "00000000"
                    response["response_msg"] = "검색 결과가 없습니다. 프로그램을 종료합니다."
                    response["data"] = [0, 0, 0, 0]
                    return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"검색 결과 처리 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)
        # 6. 완전 일치하는 항목 찾기
        try:
            matching_item = None
            search_keywords = search_address.split()

            for item in result_items:
                item_text = item.text.replace(" ", "")
                if all(keyword in item_text for keyword in search_keywords) and building_name in item_text:
                    matching_item = item
                    break

            if matching_item:
                driver.execute_script("arguments[0].scrollIntoView(true);", matching_item)
                matching_item.click()
            else:
                response["response_code"] = "90000001"
                response["response_msg"] = f"주소 {search_address}에 대한 일치 결과를 찾을 수 없습니다. 프로그램을 종료합니다."
                response["data"] = [0, 0, 0, 0]
                return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"항목 선택 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(3)

        # 7. 아파트 항목 클릭
        try:
            building_name = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "map_pop_infobox_tit1"))
            )
            apt_element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//ul[@id='aptListArea']//li/a[contains(text(), '{building_name.text}')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
            apt_element.click()
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "아파트 항목 클릭 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"아파트 항목 클릭 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

    except Exception as e:
        error = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {error}"
        response["data"] = [0, 0, 0, 0]
        return response

    return response




def rtech_app_roadnum(driver, kwargs):
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
        Doro_No = kwargs.get('Doro_No1')
        Doro_Name = kwargs.get('Doro_Name1')
        Doro_No2 = kwargs.get('Doro_No2')
        if Doro_No2 == '':
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No
        else:
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No + '-' + Doro_No2
        Chosung = kwargs.get('Chosung1')

        url = "https://www.rtech.or.kr/main/mapSearch_mp.do?popUpYn=&posX=37.48243936583027&posY=127.06183029780048#"
        driver.get(url)

        # 현재 창 정보
        main_window = driver.current_window_handle

        # 팝업 창 닫기
        try:
            for window in driver.window_handles:
                if window != main_window:
                    driver.switch_to.window(window)
                    driver.close()
            driver.switch_to.window(main_window)
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000000"
            response["response_msg"] = f"팝업 창 닫기 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        # 닫기 버튼 클릭
        try:
            close_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//area[@alt='닫기']"))
            )
            close_button.click()
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "팝업 닫기 버튼을 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"팝업 닫기 버튼 클릭 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        # 빠른검색 입력
        try:
            search_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "searchInput"))
            )
            search_address = Doro_Name2
            search_input.send_keys(search_address)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 입력 필드를 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"검색 입력 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(3)

        # 검색 결과 리스트 확인
        try:
            results_ul = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "quickSearchResult"))
            )
            result_items = results_ul.find_elements(By.TAG_NAME, "li")
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 결과 리스트를 찾을 수 없습니다."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"검색 결과 리스트 확인 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(3)

        # "검색 결과가 없습니다."
        try:
            for item in result_items:
                if "검색 결과가 없습니다." in item.text:
                    response["response_code"] = "00000000"
                    response["response_msg"] = "검색 결과가 없습니다. 프로그램을 종료합니다."
                    response["data"] = [0, 0, 0, 0]
                    return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"검색 결과 처리 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        # 완전 일치하는 항목 찾기
        try:
            matching_item = None
            search_keywords = search_address.split()

            for item in result_items:
                item_text = item.text.replace(" ", "")
                if all(keyword in item_text for keyword in search_keywords):
                    matching_item = item
                    break

            if matching_item:
                driver.execute_script("arguments[0].scrollIntoView(true);", matching_item)
                matching_item.click()
            else:
                response["response_code"] = "90000000"
                response["response_msg"] = f"주소 {search_address}에 대한 일치 결과를 찾을 수 없습니다."
                response["data"] = [0, 0, 0, 0]
                return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"항목 선택 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(3)

        # 해당 아파트 항목 클릭
        try:
            building_name = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "map_pop_infobox_tit1"))
            )
            apt_element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//ul[@id='aptListArea']//li/a[contains(text(), '{building_name.text}')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", apt_element)
            apt_element.click()
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "아파트 항목 클릭 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"아파트 항목 클릭 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

    except Exception as e:
        error = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {error}"
        response["data"] = [0, 0, 0, 0]
        return response

    return response


def captcha_APP(driver, kwargs):
    response = {
        "response_code": None,
        "response_msg": None,
        "data": None  # 하한평균가나 필요한 데이터를 반환할 필드
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
        Build_Area = kwargs.get('Build_Area1')

        # 팝업창 처리
        try:
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)
            else:
                response["response_code"] = "90000000"
                response["response_msg"] = "팝업창이 감지되지 않았습니다. 현재 화면에서 캡처를 진행합니다."
                response["data"] = [0, 0, 0, 0]
                return response
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"팝업창 처리 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(3)

        # '호별 시세조회' 요소 클릭
        try:
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
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"호별 시세조회 클릭 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(3)

        # 동 선택
        try:
            select_dong = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, 'dong_'))
            )
            select_dong = Select(select_dong)
            if not Building_No1 or Building_No1.strip() == "":
                select_dong.select_by_visible_text("동명없음")
            else:
                select_dong.select_by_visible_text(Building_No1)
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"동 선택 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(2)

        # 호 선택
        try:
            select_ho_element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'ho_code'))
            )
            select_ho = Select(select_ho_element)
            select_ho.select_by_visible_text(Room_No)
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"호 선택 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response
        
        # 기준일 가져오기
        try:
            lbAptpDt_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "lbAptpDt"))
            )

            lbAptpDt_text = lbAptpDt_element.text.strip()
            Base_Date = lbAptpDt_text.replace("시세기준일", "").strip()

        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"기준일 가져오는 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response
        
        time.sleep(2)

        # 캡차 이미지 처리
        try:
            save_path = r"C:\python\RPA\rpa\captcha_images_save"
            os.makedirs(save_path, exist_ok=True)

            page_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            page_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(page_width, page_height)
            png = driver.get_screenshot_as_png()

            captcha_img = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "captchaImg"))
            )

            # 캡차 이미지 크롭 및 저장
            element = captcha_img
            image_location = element.location
            image_size = element.size
            im = Image.open(BytesIO(png))
            left = image_location['x']
            top = image_location['y']
            right = image_location['x'] + image_size['width']
            bottom = image_location['y'] + image_size['height']
            im = im.crop((left, top, right, bottom))
            captcha_filename = os.path.join(save_path, "capcha.png")
            im.save(captcha_filename)
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"캡차 이미지 처리 중 예외 발생: {error}"
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
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"캡차 입력 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        # 확인 버튼 클릭
        try:
            confirm_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@onclick='javascript:search_dongho_price()']"))
            )
            confirm_button.click()
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"확인 버튼 클릭 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response

        time.sleep(5)

        try:
            print("alert 체크 시작")
            
            # alert 체크
            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())  # Alert 확인
                alert.accept()
                print("Alert이 감지되어 닫음")
                alert_present = True  # Alert이 감지됨
            except TimeoutException:
                print("Alert 없음")
                alert_present = False  # Alert이 없으면 False 처리

            # Alert이 떴다면
            if alert_present:
                size_background = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "pyongMarketPriceTitle"))
                )
                driver.execute_script("javascript:infotabChange(1);", size_background)

                # 공통적으로 면적을 포함하는 행을 찾음
                try:
                    time.sleep(3)
                    target_row = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(
                            (By.XPATH, f"//tr[td[normalize-space(text())='{Build_Area}']]")
                        )
                    )
                    # 해당 행의 값들 가져오기
                    element_low = target_row.find_element(By.XPATH, "./td[@class='table_txt_blue'][1]").text.strip()
                    element_high = target_row.find_element(By.XPATH, "./td[@class='table_txt_red'][1]").text.strip()
                    

                    # 쉼표 제거 및 숫자로 변환
                    rtech_low_value = int(element_low.replace(",", ""))
                    rtech_high_value = int(element_high.replace(",", ""))

                    response["response_code"] = "00000000"
                    response["response_msg"] = "정상적으로 처리되었습니다."
                    response["data"] = [0, rtech_low_value, 0, Base_Date]

                except Exception as e:
                    error = str(e).split("\n")[0]
                    response["response_code"] = "90000001"
                    response["response_msg"] = f"면적 불일치/하한평균가 가져오기 중 예외 발생: {error}"
                    response["data"] = [0, 0, 0, 0]
                    return response
            
            else: # Alert이 안떴다면
                try:
                    element_low = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "lower_trade_amt"))
                    )

                    element_low_price = element_low.text.strip()
                    # 쉼표 제거 및 숫자로 변환
                    rtech_low_value = int(element_low_price.replace(",", ""))

                    response["response_code"] = "00000000"
                    response["response_msg"] = "정상적으로 처리되었습니다."
                    response["data"] = [0, rtech_low_value, 0, Base_Date]
                except Exception as e:
                    error = str(e).split("\n")[0]
                    response["response_code"] = "90000001"
                    response["response_msg"] = f"하한평균가 가져오기 중 예외 발생: {error}"
                    response["data"] = [0, 0, 0, 0]
                    return response
            return response
        
        except Exception as e:
            error = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response
 
    except Exception as e:
        error = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {error}"
        response["data"] = [0, 0, 0, 0]
        return response

  

   