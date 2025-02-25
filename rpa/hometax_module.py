from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support.select import Select
import ssl
from selenium.common.exceptions import TimeoutException

# SSL 인증서 검증 무시 설정
ssl._create_default_https_context = ssl._create_unverified_context

def hometax_streetnum(driver, kwargs):
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
        Floor = kwargs.get('Floor1')

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

        try:
            # 페이지 로드가 완료될 때까지 기다리기
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # 덮고 있는 요소가 사라질 때까지 대기
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "mf_wq_uuid_24_mf_wq_uuid_24_wq_proessMsgModal"))
            )
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "페이지 로드 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(5)

        try: 
            # 검색창에 기준시가 입력
            search_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "w2input"))
            )
            search_input.click()
            search_input.send_keys("기준시가조회")
            time.sleep(1)
            search_input.send_keys(Keys.RETURN)  # 엔터 키 입력
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "기준시가 입력 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        try:
            # 오피스텔 및 상업용 건물 클릭
            office_building = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@id='mf_txppWframe_menu_gen_0_tbx_content' and contains(@class, 'w2textbox')]"))
            )
            office_building.click() 
            time.sleep(3)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "오피스텔 및 상업용 건물 클릭 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        try:
            # 법정동검색 클릭
            txppWframe_button = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnLdCdPop"))
            )
            txppWframe_button.click()
            time.sleep(3)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "법정동검색 클릭 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        try:
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
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "읍면동,가리 입력 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
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
                e = str(e).split("\n")[0]
                response["response_code"] = "90000001"
                response["response_msg"] = f"해당 행의 선택 버튼 없음: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
        
        time.sleep(3)

        try:
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
            time.sleep(3)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "번지/호 입력 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        # 해당 물건지 찾기
        try:
            # 모든 표시된 `txtItm` 요소 찾기
            visible_items = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//li[not(contains(@style, 'display: none;'))]//a[starts-with(@id, 'txtItm')]")
                )
            )

            # Building_Name을 포함한 항목들
            matching_items = []

            # 조건에 맞는 항목들을 matching_items에 추가
            for item in visible_items:
                item_text = item.text.strip()

                if Building_Name in item_text:
                    matching_items.append(item)

            # 만약 Building_Name을 포함한 항목이 하나라도 있으면
            if matching_items:
                # 그 중에서 building_no1을 포함한 항목을 찾는다
                for item in matching_items:
                    item_text = item.text.strip()
                    
                    if Building_No1 in item_text:
                        print(f"목표 항목 {Building_Name + Building_No1}를 찾았습니다. 클릭합니다.")
                        driver.execute_script("arguments[0].scrollIntoView();", item)
                        item.click()
                        break
                    response["response_code"] = "90000005"
                    response["response_msg"] = f"목표 항목 {Building_Name}를 찾지 못했습니다."
                    response["data"] = [0, 0, 0, 0]
                else:
                    # building_no1을 포함하지 않지만, Building_Name을 포함하는 항목이 있으면 클릭
                    print(f"목표 항목 {Building_Name}를 찾았습니다. building_no1을 포함하지 않지만 클릭합니다.")
                    item = matching_items[0]  # 첫 번째 항목을 클릭
                    driver.execute_script("arguments[0].scrollIntoView();", item)
                    item.click()

            else:
                # Building_Name을 포함한 항목을 찾지 못한 경우
                response["response_code"] = "90000005"
                response["response_msg"] = f"목표 항목 {Building_Name + Building_No1}를 찾지 못했습니다."
                response["data"] = [0, 0, 0, 0]
                return response

        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"해당 물건지 찾기 도중 에러발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        
        # 상세주소 검색
        # 동
        select_dong = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldComp'))
        )
        select = Select(select_dong)
        # 옵션 목록 가져오기
        options = select.options
        time.sleep(1)
        # 동 옵션이 2개뿐이라면 자동 선택(선택하세요, 1(단일))
        if len(options) == 2:
            select.select_by_index(1) 
        # Building_No1이 빈 값이면 첫 번째 옵션 선택
        elif not Building_No1 or Building_No1.strip() == "":
            select.select_by_index(1)
        else:
            # Building_No1 값으로 선택
            try:
                for option in options:
                    if Building_No1 in option.text:
                        select.select_by_visible_text(option.text)
                        break
                response["response_code"] = "90000001"
                response["response_msg"] = "동 선택하는 데 실패했습니다"
                response["data"] = [0, 0, 0, 0]
            
            except Exception as e:
                e = str(e).split("\n")[0]
                response["response_code"] = "90000001"
                response["response_msg"] = f"{Building_No1} 값으로 선택하는 데 실패했습니다: {e}"
                response["data"] = [0, 0, 0, 0]
                return response

        try:
            # 층
            select_floor = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldFlor'))
            )
            select_1 = Select(select_floor)
            select_1.select_by_visible_text(Floor)
            time.sleep(2)
            # 호
            select_ho = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldHo'))
            )
            select_2 = Select(select_ho)
            # 선택 가능한 모든 옵션 가져오기
            options = select_2.options
            for option in options:
                if Room_No in option.text:  # "201"이 포함된 텍스트를 찾아 선택
                    select_2.select_by_visible_text(option.text)
                    break

            
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"층/호 선택하는 데 실패했습니다: {e}"
            response["data"] = [0, 0, 0, 0]
            return response

        try:
            # 검색버튼 클릭
            mf_txppWframe_btnSchTsv= WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnSchTsv"))
            )
            driver.execute_script("arguments[0].click();", mf_txppWframe_btnSchTsv)
            time.sleep(5)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색버튼 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        try:
            # 1. 단위면적 당 기준시가 
            price_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='notcPrc']/nobr"))
            )
            raw_price = price_element.text.strip()  # '4,761,000'
            hometax_price_value = int(raw_price.replace(",", ""))  # 쉼표 제거 후 숫자로 변환

            # 2. 견물면적 
            size_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='bldTotaSfl']/nobr"))
            )
            raw_size = size_element.text.strip()  # '36.4'
            hometax_size_value = float(raw_size)  # 실수로 변환

            # 기준일
            date_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='notcDt']/nobr"))
            )
            date_value = date_element.text.strip() 

            response["response_code"] = "00000000"
            response["response_msg"] = "정상적으로 처리되었습니다."
            response["data"] = [hometax_price_value, 0, hometax_size_value, date_value]

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색버튼 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    return response

def hometax_roadnum(driver, kwargs):
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
            Doro_Name2 = kwargs.get('Doro_Name1') + '' + Doro_No
        else:
            Doro_Name2 = kwargs.get('Doro_Name1') + '' + Doro_No + '-' + Doro_No2
        Chosung = kwargs.get('Chosung1')
        Floor = kwargs.get('Floor1')

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

        try:
            # 페이지 로드가 완료될 때까지 기다리기
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # 덮고 있는 요소가 사라질 때까지 대기
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "mf_wq_uuid_24_mf_wq_uuid_24_wq_proessMsgModal"))
            )
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "페이지 로드 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        time.sleep(3)

        try:
            # 검색창에 기준시가 입력
            search_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "w2input"))
            )
            search_input.click()
            search_input.send_keys("기준시가조회")
            time.sleep(1)
            search_input.send_keys(Keys.RETURN)  # 엔터 키 입력
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "기준시가 입력 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        try:
            # 오피스텔 및 상업용 건물 클릭
            office_building = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@id='mf_txppWframe_menu_gen_0_tbx_content' and contains(@class, 'w2textbox')]"))
            )
            office_building.click() 
            time.sleep(3)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "오피스텔 및 상업용 건물 클릭 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 

        try:
            # 도로명주소로 조회 클릭
            raod_click = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='mf_txppWframe_rdoByRoadNmCd_input_0']"))
            )
            # 요소 클릭
            raod_click.click()
            time.sleep(3)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "도로명주소로 조회 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        try:
            # 도로명주소 입력
            mf_txppWframe_txtRoadNm = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "mf_txppWframe_txtRoadNm"))
            )
            mf_txppWframe_txtRoadNm.send_keys(Doro_Name)
            time.sleep(3)

            # 검색 클릭
            mf_txppWframe_btnSchRoadNm= WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnSchRoadNm"))
            )
            driver.execute_script("arguments[0].click();", mf_txppWframe_btnSchRoadNm)
            time.sleep(3)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "도로명주소로 검색 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        # 해당 도로명 주소 찾기
        try:
            
            # 페이지 값 가져오기 
            mf_txppWframe_txtTotalPage0= WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "mf_txppWframe_txtTotalPage0"))
            )
            txtTotalPage0 = mf_txppWframe_txtTotalPage0.get_attribute("innerText").strip()
            #print(f"총 페이지 수: {txtTotalPage0}")
            time.sleep(2)

            # 해당 물건지 찾았는지 상태값
            FindFlag = False
            # 페이지 개수만큼 반복
            for page in range(1, int(txtTotalPage0) + 1):
                # 모든 표시된 `txtRdNmItm0` 요소 찾기
                visible_items = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//li[not(contains(@style, 'display: none;'))]//a[starts-with(@id, 'txtRdNmItm')]")
                    )
                )
             
                time.sleep(2)

                # 각 요소의 텍스트 확인
                for item in visible_items:
                    item = item.text.strip()    
                    #print(item)

                    if Ridong in item and Doro_Name in item:
                        FindFlag = True
                        print(f"목표 항목 {Ridong}를 찾았습니다. 클릭합니다.")
                        # 해당 항목을 찾음
                        target_element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{item}')]"))
                        )
                        target_element.click()
                        break                
           
                # 페이징 클릭
                if not FindFlag:                
                    next_page_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.ID, f"mf_txppWframe_pglNavi0_page_{page+1}"))
                    )
                    driver.execute_script("arguments[0].click();", next_page_button)
                    time.sleep(2) 

            if not FindFlag:                
                response["response_code"] = "90000005"
                response["response_msg"] = f"목표 항목 {Ridong, Doro_Name}를 찾지 못했습니다."
                response["data"] = [0, 0, 0, 0]
                return response 
    
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = "해당 물건지 찾기 오류 발생." + e
            response["data"] = [0, 0, 0, 0]
            return response 

        time.sleep(3)

        # 해당 건물명 클릭
        try:
            # 모든 표시된 `txtItm` 요소 찾기
            visible_items = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//li[not(contains(@style, 'display: none;'))]//a[starts-with(@id, 'txtItm')]")
                )
            )

            # Building_Name을 포함한 항목들
            matching_items = []

            # 조건에 맞는 항목들을 matching_items에 추가
            for item in visible_items:
                item_text = item.text.strip()

                if Building_Name in item_text:
                    matching_items.append(item)

            # 만약 Building_Name을 포함한 항목이 하나라도 있으면
            if matching_items:
                # 그 중에서 building_no1을 포함한 항목을 찾는다
                for item in matching_items:
                    item_text = item.text.strip()
                    if Building_No1 in item_text:
                        print(f"목표 항목 {Building_Name + Building_No1}를 찾았습니다. 클릭합니다.")
                        driver.execute_script("arguments[0].scrollIntoView();", item)
                        item.click()
                        break
                    response["response_code"] = "90000005"
                    response["response_msg"] = f"목표 항목 {Building_Name}를 찾지 못했습니다."
                    response["data"] = [0, 0, 0, 0]
                else:
                    # building_no1을 포함하지 않지만, Building_Name을 포함하는 항목이 있으면 클릭
                    print(f"목표 항목 {Building_Name}를 찾았습니다. building_no1을 포함하지 않지만 클릭합니다.")
                    item = matching_items[0]  # 첫 번째 항목을 클릭
                    driver.execute_script("arguments[0].scrollIntoView();", item)
                    item.click()

            else:
                # Building_Name을 포함한 항목을 찾지 못한 경우
                response["response_code"] = "00000000"
                response["response_msg"] = f"목표 항목 {Building_Name + Building_No1}를 찾지 못했습니다."
                response["data"] = [0, 0, 0, 0]
                return response

        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"해당 물건지 찾기 도중 에러발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response

        # 상세주소 검색
        # 동
        select_dong = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldComp'))
        )
        select = Select(select_dong)
        # 옵션 목록 가져오기
        options = select.options
        time.sleep(1)
        # 동 옵션이 2개뿐이라면 자동 선택(선택하세요, 1(단일))
        if len(options) == 2:
            select.select_by_index(1) 
        # Building_No1이 빈 값이면 첫 번째 옵션 선택
        elif not Building_No1 or Building_No1.strip() == "":
            select.select_by_index(1)
        else:
            # Building_No1 값으로 선택
            try:
                options = select.options
                for option in options:
                    if Room_No in option.text:
                        select.select_by_visible_text(option.text)
                        break
                response["response_code"] = "90000001"
                response["response_msg"] = "동 선택하는 데 실패했습니다"
                response["data"] = [0, 0, 0, 0]
            

            except Exception as e:
                e = str(e).split("\n")[0]
                response["response_code"] = "90000001"
                response["response_msg"] = f"{Building_No1} 값으로 선택하는 데 실패했습니다: {e}"
                response["data"] = [0, 0, 0, 0]
                return response
    
        try:
            # 층
            select_floor = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldFlor'))
            )
            select_1 = Select(select_floor)
            select_1.select_by_visible_text(Floor)
            time.sleep(2)
            # 호
            select_ho = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'mf_txppWframe_selBldHo'))
            )
            select_2 = Select(select_ho)
            time.sleep(2)
            # 선택 가능한 모든 옵션 가져오기
            options = select_2.options
            for option in options:
                if Room_No in option.text:  # "201"이 포함된 텍스트를 찾아 선택
                    select_2.select_by_visible_text(option.text)
                    break
            response["response_code"] = "90000001"
            response["response_msg"] = "층/호 선택하는 데 실패했습니다"
            response["data"] = [0, 0, 0, 0]

        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"층/호 선택하는 데 실패했습니다: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        
        try:
            # 검색버튼 클릭
            mf_txppWframe_btnSchTsv= WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "mf_txppWframe_btnSchTsv"))
            )
            driver.execute_script("arguments[0].click();", mf_txppWframe_btnSchTsv)
            time.sleep(5)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색버튼 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        try:
            # 1. 단위면적당 기준시가가
            price_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='notcPrc']/nobr"))
            )
            raw_price = price_element.text.strip()
            hometax_price_value = int(raw_price.replace(",", ""))  # 쉼표 제거 후 숫자로 변환

            # 2. 건물면적적
            size_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='bldTotaSfl']/nobr"))
            )
            raw_size = size_element.text.strip()  
            hometax_size_value = float(raw_size) 

            # 기준일
            date_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//td[@data-col_id='notcDt']/nobr"))
            )
            date_value = date_element.text.strip() 

            response["response_code"] = "00000000"
            response["response_msg"] = "정상적으로 처리되었습니다."
            response["data"] = [hometax_price_value, 0, hometax_size_value, date_value]

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "단위면적당/건물면적 조회 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response 

    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"프로세스 실행 중 알 수 없는 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    return response
