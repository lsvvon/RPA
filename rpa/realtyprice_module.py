from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException

# 공동주택(아파트, 다세대)일 경우 - 지번 검색
def realtyprice_apt_streetnum(driver, kwargs):
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
        Room_No = kwargs.get('Room_No1')

        url = "https://www.realtyprice.kr/notice/main/mainBody.htm"
        driver.get(url)

        # 페이지 로드 대기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 팝업 처리
        try:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#wrap_pop_no iframe.b-iframe"))
            )
            driver.switch_to.frame(iframe)

            close_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@onclick, 'closeWin')]"))
            )
            driver.execute_script("arguments[0].click();", close_button)
            driver.switch_to.default_content()
        except TimeoutException:
            driver.switch_to.default_content()
        except Exception as e:
            print(f"모달 닫기 중 예외 발생: {e}")
            driver.switch_to.default_content()

        # 팝업 창 닫기
        main_window = driver.current_window_handle
        for window in driver.window_handles:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(main_window)

        # "공동주택공시가격" 페이지 이동
        link_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='공동주택공시가격']"))
        )
        link_element.click()
        time.sleep(3)
        # 지번 검색 클릭
        zibun_search = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='지번검색']"))
        )
        zibun_search.click()
        time.sleep(3)

        # 시/도, 시/군/구, 읍/면/동 선택
        try:
            select = Select(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'sido_list'))))
            select.select_by_visible_text(Sido)
            time.sleep(3)
            select_1 = Select(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'sgg_list'))))
            select_1.select_by_visible_text(Sigungu2)
            time.sleep(3)
            select_2 = Select(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'eub_list'))))
            select_2.select_by_visible_text(Ridong)
            time.sleep(3)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)
        # 지번 입력
        try:
            radio_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='rdoCondi' and @value='1']"))
            )
            driver.execute_script("arguments[0].click();", radio_button)
            time.sleep(2)
            bun1 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='bun1' and @class='text2']"))
            )
            bun1.send_keys(Jibun_No1)
            time.sleep(2)
            bun2 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='bun2' and @class='text2']"))
            )
            bun2.send_keys(Jibun_No2)
            time.sleep(2)
            search_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@class, 'btn-src1')]"))
            )
            driver.execute_script("searchAptName(1);", search_button)
            time.sleep(2)
            if bun2.get_attribute("value") == '0':
                # 검색 클릭            
                search_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@class, 'btn-src1')]"))
                )
                driver.execute_script("searchAptName(1);", search_button)

            time.sleep(2)

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "지번 입력 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(2)
        # 단지명 클릭
        try:
            apt = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'apt')))
            select_3 = Select(apt)
            for option in select_3.options:
                if Building_Name in option.text:
                    select_3.select_by_visible_text(option.text)
                    break
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "단지명 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(2)
        # 동, 호 선택
        try:
            dong = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'dong')))
            select_4 = Select(dong)
            if not Building_No1 or Building_No1.strip() == "":
                select_4.select_by_index(0)
            else:
                select_4.select_by_visible_text(Building_No1)

            time.sleep(2)

            ho = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'ho')))
            select_5 = Select(ho)
            select_5.select_by_visible_text(Room_No)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "동/호 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        
        time.sleep(2)

        # 열람하기 클릭
        try:
            show_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@class, 'btn-src3')]"))
            )
            driver.execute_script("goPage('1')", show_button)
            time.sleep(2)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "열람하기 클릭 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        
        time.sleep(2)
        # 공동주택가격 값 가져오기
        try:
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "opinNoticeAmt"))
            )
            realty_value = int(element.text.strip().replace(",", ""))

            element_1 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#dataList tr:first-child td:nth-child(5)"))
            )
            area_value = float(element_1.text.strip().replace(",", ""))

            date_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//tbody[@id='dataList']/tr[1]/td[1]"))
            )
            date_value = date_element.text

            response["response_code"] = "00000000"
            response["response_msg"] = "정상적으로 처리되었습니다."
            response["data"] = [realty_value, 0, area_value, date_value]

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "공동주택가격 값을 가져오는 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"공동주택가격 값을 가져오는 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"프로세스 실행 중 알 수 없는 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    return response


def realtyprice_apt_roadnum(driver, kwargs):
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
        Doro_No = kwargs.get('Doro_No1')
        Doro_Name = kwargs.get('Doro_Name1')
        Doro_No2 = kwargs.get('Doro_No2')
        if Doro_No2 == '':
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No
        else:
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No + '-' + Doro_No2
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

        time.sleep(2)

        try:
            # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
            sido_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sido'))
            )
            select = Select(sido_list)
            select.select_by_visible_text(Sido)

            time.sleep(2)
            sgg_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sigungu'))
            )
            select_1 = Select(sgg_list)
            select_1.select_by_visible_text(Sigungu)

            time.sleep(2)
            eub_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'initialword'))
            )
            select_2 = Select(eub_list)
            select_2.select_by_visible_text(Chosung)

            time.sleep(2)
            road_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'road'))
            )
            select_3 = Select(road_list)
            select_3.select_by_visible_text(Doro_Name)

        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"주소 검색 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)

        # 단지명 클릭
        try:
            apt = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'apt'))
            )
            select_4 = Select(apt)
            for option in select_4.options:
                if Building_Name in option.text:  # Building_Name이 포함된 텍스트를 찾음
                    select_4.select_by_visible_text(option.text)
                    break
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"단지명 선택 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "단지명 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(2)

        try:
            # 동 클릭
            dong = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'dong'))
            )
            select_4 = Select(dong)
            # Building_No1이 빈값인지 확인
            if not Building_No1 or Building_No1.strip() == "":
                select_4.select_by_index(0)  # 첫 번째 값 선택
            else:
                select_4.select_by_visible_text(Building_No1)  # Building_No1 값 선택
            time.sleep(2)
            # 호 클릭
            ho = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'ho'))
            )
            select_5 = Select(ho)
            select_5.select_by_visible_text(Room_No)
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"동/호 선택 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "동/호 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)

        # 열람하기 클릭
        try:
            show_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@class, 'btn-src3')]"))
            )
            driver.execute_script("goPage('1')", show_button)
            time.sleep(2)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "열람하기 클릭 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        
        time.sleep(2)
        # 공동주택가격 값
        try:
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "opinNoticeAmt"))
            )
            
            # 값 추출 및 공백 제거
            raw_text = element.text.strip()
            # 쉼표 제거 및 숫자로 변환
            realty_value = int(raw_text.replace(",", ""))
            # 전용면적 값
            element_1 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#dataList tr:first-child td:nth-child(5)"))
            )
            # 값 추출 및 공백 제거
            element_1_text = element_1.text.strip()
            # 쉼표 제거 및 숫자로 변환
            area_value = float(element_1_text.replace(",", ""))

            # 기준일 값
            date_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//tbody[@id='dataList']/tr[1]/td[1]"))
            )

            date_value = date_element.text

            response["response_code"] = "00000000"
            response["response_msg"] = "정상적으로 처리되었습니다."
            response["data"] = [realty_value, 0, area_value, date_value]

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "공동주택가격 값을 가져오는 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"공동주택가격 값을 가져오는 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        
    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"프로세스 실행 중 알 수 없는 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    return response

def realtyprice_individual_streetnum(driver, kwargs):
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

        time.sleep(2)

        try:
            # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
            sido_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sido_list'))
            )
            select = Select(sido_list)
            select.select_by_visible_text(Sido)

            time.sleep(2)
            sgg_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sgg_list'))
            )
            select_1 = Select(sgg_list)
            select_1.select_by_visible_text(Sigungu2)

            time.sleep(2)
            eub_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'eub_list'))
            )
            select_2 = Select(eub_list)
            select_2.select_by_visible_text(Ridong)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(2)

        try:
            # 번지 입력
            bun1 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='bun1' and @class='text3']"))
            )
            driver.execute_script("arguments[0].click();", bun1)
            bun1.send_keys(Jibun_No1)

            time.sleep(2)
            bun2 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='bun2' and @class='text3']"))
            )
            driver.execute_script("arguments[0].click();", bun2)
            bun2.send_keys(Jibun_No2)

            # 검색 클릭            
            search_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@alt, '검색')]"))
            )
            driver.execute_script("goPage(1)", search_button)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "지번 입력 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(2)

        try:
            # XPath를 사용해 <tr> 태그 내부의 마지막 <td> 값(개별주택가격)을 가져옴
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//tr/td[last()]"))
            )
            
            # 텍스트 추출
            raw_text = element.text.strip()
            
            # 쉼표 제거 및 숫자로 변환
            realty_value = int(raw_text.replace(",", ""))
            
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

            response["response_code"] = "00000000"
            response["response_msg"] = "정상적으로 처리되었습니다."
            response["data"] = [realty_value, 0, area_value, date_value]

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "개별주택가격 값을 가져오는 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"개별주택가격 값을 가져오는 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response

    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"프로세스 실행 중 알 수 없는 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    return response  

def realtyprice_individual_roadnum(driver, kwargs):
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
        Doro_No = kwargs.get('Doro_No1')
        Doro_No2 = kwargs.get('Doro_No2')
        Doro_Name = kwargs.get('Doro_Name1')
        Doro_No2 = kwargs.get('Doro_No2')
        if Doro_No2 == '':
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No
        else:
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No + '-' + Doro_No2
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

        time.sleep(2)
        road_search = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='도로명검색']"))
        )
        road_search.click() 

        time.sleep(2)

        try:
            # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
            sido_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'area1'))
            )
            select = Select(sido_list)
            #select.select_by_index(1)
            select.select_by_visible_text(Sido)

            time.sleep(2)
            sgg_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sigungu'))
            )
            select_1 = Select(sgg_list)
            select_1.select_by_visible_text(Sigungu)

            time.sleep(2)
            eub_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'initialword'))
            )
            select_2 = Select(eub_list)
            select_2.select_by_visible_text(Chosung)

            time.sleep(2)
            road_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'road'))
            )
            select_3 = Select(road_list)
            select_3.select_by_visible_text(Doro_Name)

        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"주소 검색 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(2)

        try:
            # 건물번호 -> 도로명 번호로 입력
            bun1 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun1' and @class='text3 input_number_only']"))
            )
            driver.execute_script("arguments[0].click();", bun1)
            bun1.send_keys(Doro_No)

            bun2 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun2' and @class='text3 input_number_only']"))
            )
            driver.execute_script("arguments[0].click();", bun2)
            bun2.send_keys(Doro_No2)


            time.sleep(2)
            # 검색 클릭            
            search_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='image' and contains(@alt, '검색')]"))
            )
            driver.execute_script("goPage(1)", search_button)
            
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "건물번호 입력 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(2)

        try:
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//tr/td[last()]"))
            )

            raw_text = element.text.strip()
            
            # 쉼표 제거 및 숫자로 변환
            realty_value = int(raw_text.replace(",", ""))
            
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
            response["response_code"] = "00000000"
            response["response_msg"] = "정상적으로 처리되었습니다."
            response["data"] = [realty_value, 0, area_value, date_value]

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "개별주택가격 값을 가져오는 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"개별주택가격 값을 가져오는 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
            
      
    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"프로세스 실행 중 알 수 없는 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    return response

def realtyprice_land_streetnum(driver, kwargs):
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

        time.sleep(2)
        try:
            # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
            sido_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sido_list'))
            )
            select = Select(sido_list)
            select.select_by_visible_text(Sido)

            time.sleep(2)
            sgg_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sgg_list'))
            )
            select_1 = Select(sgg_list)
            select_1.select_by_visible_text(Sigungu2)

            time.sleep(2)
            eub_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'eub_list'))
            )
            select_2 = Select(eub_list)
            select_2.select_by_visible_text(Ridong)
        
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(2)

        try:
            # 지번 입력
            bun1 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='bun1' and @class='text3']"))
            )
            driver.execute_script("arguments[0].click();", bun1)
            bun1.send_keys(Jibun_No1)

            time.sleep(2)
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

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "지번 입력 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)

        try:
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//tr/td[4]"))
            )

            raw_text = element.text.strip() 

            # 쉼표와 단위 제거 및 숫자로 변환
            realty_land_value = int(raw_text.replace(",", "").split(" ")[0])  # 쉼표 제거 후 '원/㎡' 분리
            response["response_code"] = "00000000"
            response["response_msg"] = "정상적으로 처리되었습니다."
            response["data"] = [realty_land_value, 0, 0, 0]           
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "개별주택가격 값을 가져오는 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"개별공시지가 값을 가져오는 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        
    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"프로세스 실행 중 알 수 없는 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    return response  

def realtyprice_land_roadnum(driver, kwargs):
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
        Doro_No = kwargs.get('Doro_No1')
        Doro_No2 = kwargs.get('Doro_No2')
        Doro_Name = kwargs.get('Doro_Name1')
        Doro_No2 = kwargs.get('Doro_No2')
        if Doro_No2 == '':
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No
        else:
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No + '-' + Doro_No2
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
            response["response_code"] = "90000000"
            response["response_msg"] = "모달 닫기 버튼이 존재하지 않음."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"모달 닫기 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response

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

        time.sleep(2)

        try:
            # 시/도 선택, 시/군/구 선택, 읍/면/동 선택
            sido_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'area1'))
            )
            select = Select(sido_list)
            select.select_by_visible_text(Sido)

            time.sleep(2)
            sgg_list = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'sigungu'))
            )
            select_1 = Select(sgg_list)
            select_1.select_by_visible_text(Sigungu)

            time.sleep(2)
            initialword = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'initialword'))
            )
            select_2 = Select(initialword)
            select_2.select_by_visible_text(Chosung)

            time.sleep(2)
            road = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'road'))
            )
            select_3 = Select(road)
            select_3.select_by_visible_text(Doro_Name)

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 선택 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)

        try:
            # 건물번호 -> 도로명 번호로 입력
            bun1 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun1' and @class='text3 input_number_only']"))
            )
            driver.execute_script("arguments[0].click();", bun1)
            bun1.send_keys(Doro_No)

            bun2 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='build_bun2' and @class='text3 input_number_only']"))
            )
            driver.execute_script("arguments[0].click();", bun2)
            bun2.send_keys(Doro_No2)

            time.sleep(2)
            
            # '검색' 버튼 가져오기
            search_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='image' and @alt='검색']"))
            )

            # 버튼 클릭
            search_button.click()

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "지번 입력 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)

        try:
            element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//tr/td[4]"))
            )
            raw_text = element.text.strip()
            
            # 쉼표와 단위 제거 및 숫자로 변환
            realty_land_value = int(raw_text.replace(",", "").split(" ")[0])  # 쉼표 제거 후 '원/㎡' 분리
            response["response_code"] = "00000000"
            response["response_msg"] = "정상적으로 처리되었습니다."
            response["data"] = [realty_land_value, 0, 0, 0]             
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "개별공시지가 값을 가져오는 중 타임아웃 발생"
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"개별공시지가 값을 가져오는 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
                
    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"프로세스 실행 중 알 수 없는 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    return response


