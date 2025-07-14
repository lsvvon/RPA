from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import re
import difflib

# 지번 검색
def KBland_streetnum(driver, dataloop, kwargs):
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
        Build_Area = kwargs.get('Build_Area1')
        Estate_Gubun1 = kwargs.get('Estate_Gubun1')

        url = "https://kbland.kr/home"
        driver.get(url)

        # 팝업창 종료
        main = driver.window_handles
        for i in main:
            if i != main[0]:
                driver.switch_to.window(i)
                driver.close()

        # 페이지 로드 확인
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "페이지 로드 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response

        # 주소 입력 영역
        try:
            input_div = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "input-land")))
            driver.execute_script("arguments[0].click();", input_div)
            
            time.sleep(1)

            input_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control")))

            address_parts = [
                Ridong.strip() if Ridong else "",
                Jibun_No1.strip() if Jibun_No1 else "",
                Jibun_No2.strip() if Jibun_No2 else ""
            ]
            address = f"{address_parts[0]} {address_parts[1]}-{address_parts[2]}".strip()
            if address.endswith("-"):
                address = address[:-1]
            
            input_element.send_keys(address)         
            input_element.send_keys(Keys.ENTER)

            time.sleep(1)
        
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 입력 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"주소 입력 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response
      
        def parse_cost_value(text):
            text = text.replace(",", "")  # 숫자에 있는 콤마 제거
            match = re.match(r"(?:(\d+)억)?\s*(?:(\d+)만)?", text)
            if match:
                billion = int(match.group(1)) * 10**8 if match.group(1) else 0
                million = int(match.group(2)) * 10**4 if match.group(2) else 0
                return billion + million
            
            return 0

        # 상세시세에서 면적 클릭히고 해당하는 대상 선택한다. 시세를 가져온다.   
        def proceed_with_area_selection(driver, Build_Area, response):
            try:
                # time.sleep(3)

                # 면적 클릭해서 리스트 가져오기
                area_select_div = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".widthTypeValue")))
                driver.execute_script("arguments[0].click();", area_select_div)
                time.sleep(1)  

                # 타이틀 시세, KB AI시세 구분하기
                detailTit_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "thbox.txcenter")))
                detailTit_element = detailTit_element.text.strip()

                # 타이틀에 AI 있는지 체크해서 분기한다. 문자열 어디에든 정규식과 일치하는 부분이 있는지 확인합니다
                search = re.search("AI", detailTit_element) 
                if search:         
                    # KB AI시세            
                    # 면적 리스트
                    try: 
                        area_elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tdbold")))
                        area_list = [element.text for element in area_elements]

                    except NoSuchElementException:
                        print("요소를 찾을 수 없습니다.[KB AI시세 면적 리스트]")                          
                    
                    # 해당 면적 선택 여부
                    build_flag = False

                    try:
                        for i in range(len(area_list)):                    
                            if Build_Area in area_list[i]:
                                area_select = driver.find_elements(By.CLASS_NAME, "tdbold")[i]
                                driver.execute_script("arguments[0].click();", area_select)
                                build_flag = True
                                break

                        # 면적없음            
                        if build_flag == False:
                            response["response_code"] = "90000000"
                            response["response_msg"] = "면적을 찾을 수 없음."
                            response["data"] = [0, 0, 0, 0]
                            return response
                        
                    except NoSuchElementException:
                        print("요소를 찾을 수 없습니다.[KB AI시세 면적 리스트]")  

                    time.sleep(1) 

                    # 시세가 없습니다. 여부
                    noDataTxt_flag = True
                    # <div data-v-607e079f="" class="noDataTxt">시세가 없습니다.</div>
                    # 면적을 클릭하고 상세시세에 시세가 없습니다. 인 경우 체크 로직 추가                
                    try:
                        # 객체 찾기 :: 시세가 없습니다.
                        noDataTxt_element = driver.find_element(By.CSS_SELECTOR, ".noDataTxt")
                        #noDataTxt_text = noDataTxt_element.text.strip()
                        #print("요소가 존재합니다.")
                        noDataTxt_flag = False
                    
                        response["response_code"] = "90000004"
                        response["response_msg"] = "시세가 없습니다. [KB AI시세]"
                        response["data"] = [0, 0, 0, 0]
                        return response           

                    except NoSuchElementException:
                        print("요소를 찾을 수 없습니다.")  

                    # 시세가 없습니다. 아닌 경우 시세가 있는 경우 처리
                    if noDataTxt_flag:
                        common_value_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".costvalue")))
                        common_value_text = common_value_element.text.strip()     

                        if "시세없음" in common_value_text:  # 시세없음인 경우 0 반환
                            kb_common_value = 0
                            kb_low_value = 0
                            date_text = 0

                            response["response_code"] = "90000008"
                            response["response_msg"] = "검색결과 시세없음."
                            response["data"] = [kb_common_value, kb_low_value, 0, date_text]            
                            return response
                            # print("일반가 값이 '시세없음'이므로 일반가와 하위평균가를 0으로 설정합니다.")
                        else:
                            kb_common_value = parse_cost_value(common_value_text)                        
                            # 하위평균가 가져오기
                            low_value_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[em[text()='하위평균가']]")))
                            low_value_text = low_value_element.text.replace("하위평균가", "").strip()
                            kb_low_value = parse_cost_value(low_value_text)
                            # 기준일 가져오기
                            date_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='text-1e1e1e']")))
                            date_text = date_element.text.replace("’", "").strip()

                    response["response_code"] = "90000003"
                    response["response_msg"] = "KB AI시세."
                    response["data"] = [kb_common_value, kb_low_value, 0, date_text] 
                    return response

                else:
                    # 시세
                    # 면적 리스트 
                    area_elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tdbold")))
                    area_list = [element.text for element in area_elements]
                
                    # 해당 면적 선택 여부
                    build_flag = False

                    for i in range(len(area_list)):                    
                        if Build_Area in area_list[i]:
                            area_select = driver.find_elements(By.CLASS_NAME, "tdbold")[i]
                            driver.execute_script("arguments[0].click();", area_select)
                            build_flag = True
                            break

                    # 면적없음            
                    if build_flag == False:
                        response["response_code"] = "90000000"
                        response["response_msg"] = "면적을 찾을 수 없음."
                        response["data"] = [0, 0, 0, 0]
                        return response
                    
                    time.sleep(1)

                    common_value_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".costvalue")))
                    common_value_text = common_value_element.text.strip()       

                    if "시세없음" in common_value_text:  # 시세없음인 경우 0 반환
                        kb_common_value = 0
                        kb_low_value = 0
                        date_text = 0

                        response["response_code"] = "90000008"
                        response["response_msg"] = "검색결과 시세없음."
                        response["data"] = [kb_common_value, kb_low_value, 0, date_text]            
                        return response
                        # print("일반가 값이 '시세없음'이므로 일반가와 하위평균가를 0으로 설정합니다.")
                    else:
                        kb_common_value = parse_cost_value(common_value_text)
                        # 하위평균가 가져오기
                        low_value_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[em[text()='하위평균가']]")))
                        low_value_text = low_value_element.text.replace("하위평균가", "").strip()
                        kb_low_value = parse_cost_value(low_value_text)
                        # 기준일 가져오기
                        date_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='costdate']")))
                        date_text = date_element.text.replace("’", "").strip()

                    # 특정 요소를 페이지 상단으로 스크롤 이동
                    element = driver.find_element(By.XPATH, "//*[@class='saleBar']")                    
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)

                    response["response_code"] = "00000000"
                    response["response_msg"] = "정상적으로 처리되었습니다."
                    response["data"] = [kb_common_value, kb_low_value, 0, date_text]            
                    return response

            except TimeoutException:
                response["response_code"] = "90000000"
                response["response_msg"] = "시세조회 타임아웃 발생."
                response["data"] = [0, 0, 0, 0]
                return response
            except Exception as e:
                error = str(e).split(";")[0]
                error = str(error).split("\n")[0]
                response["response_code"] = "90000001"
                response["response_msg"] = f"예상치 못한 오류 발생: {error}"
                response["data"] = [0, 0, 0, 0]
                return response
            
        # 검색 결과 처리
        try:
            WebDriverWait(driver, 10).until(
                EC.any_of(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".item-search-poi")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".widthTypeValue")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".nodata"))
                )
            )

            if driver.find_elements(By.CSS_SELECTOR, ".nodata"):
                nodata_message = driver.find_element(By.CSS_SELECTOR, ".nodata").text.strip()
                response["response_code"] = "90000005"
                response["response_msg"] = f"검색 결과가 없습니다: {nodata_message}"
                response["data"] = [0, 0, 0, 0]
                return response

            # ==============================================================================================
            # 주소검색해서 1건 나오는 경우 상세화면으로 바로 넘어가는데 면적 객체가(widthTypeValue) 있으면 상세화면으로 인식하고 면적 클릭으로 넘어간다. 콜 함수에서 면적에 해당건 가져온다.            
            # ==============================================================================================
            if driver.find_elements(By.CSS_SELECTOR, ".widthTypeValue"):
                return proceed_with_area_selection(driver, Build_Area, response)
            
            # ==============================================================================================
            # 주소검색해서 2건이상 나오는 경우 리스트에서 선텍한다.
            # ==============================================================================================
            items = driver.find_elements(By.CSS_SELECTOR, ".item-search-poi")

            # 물건지 : 1 주상복합 아파트, 4 오피스텔 2 다세대 및 연립주택, 3 기타(단독주택, 다가구주택) 객체명 처리
            if Estate_Gubun1 == "1":
                Estate_class = "ico-poi.ico-apt"
                Estate_Name = "주상복합"
                Estate_Name2 = "아파트"
            if Estate_Gubun1 == "4":
                Estate_class = "ico-poi.ico-officetel"
                Estate_Name = "오피스텔"
            if Estate_Gubun1 == "2":
                Estate_class = "ico-poi.ico-officetel"
                Estate_Name = "연립주택"
                Estate_Name2 = "다세대"
            if Estate_Gubun1 == "3":
                Estate_class = "ico-poi.ico-officetel"
                Estate_Name = "단독주택"
                Estate_Name2 = "다가구주택"       

            #<span data-v-2e001bba="" class="ico-poi ico-apt">주상복합</span>
            #<span data-v-2e001bba="" class="ico-poi ico-officetel">오피스텔</span>
            # Estate_class.replace(" ", ".")

            Building_Name3 = ""
            # 건물명 동 선처리(건물명에 동이 있는 경우) 마지막에 동만 제거한다. 
            Ridong3 = re.sub("동$", "", Ridong)
            # 마지막 동 제거하고 건물명에 있으면 치환한다.
            match = re.match(Ridong3, Building_Name) 
            if match:
                Building_Name3 = Building_Name.replace(Ridong3, Ridong)

            # 아파트 포함인 경우 
            Building_Name4 = re.sub("아파트$", "", Building_Name)
            
            if items:
                for item in items:
                    try:
                        # 객체 찾기 :: 물건지 처리
                        Estate_element = item.find_element(By.CSS_SELECTOR, "." + Estate_class)
                        Estate_text = Estate_element.text.strip()
                        #print("요소가 존재합니다.")
                    except NoSuchElementException:
                        #print("요소를 찾을 수 없습니다.")
                        continue  # 요소가 없는 경우 건너뛰고, 다음 반복으로 넘어감
                    
                    # 건물명
                    name_element = item.find_element(By.CSS_SELECTOR, ".text")
                    name_text = name_element.text.strip()                    

                    # 1.건물명(건물명에 동이 있는경우 동 제외인 경우), 물건지 필터링
                    if Building_Name in name_text and (Estate_Name in Estate_text or Estate_Name2 in Estate_text):
                        name_element.click()                      
                        return proceed_with_area_selection(driver, Build_Area, response)
                    
                    # 2.건물명(건물명에 동이 있는경우 동 포함해야 하는 경우), 물건지 필터링
                    if Building_Name3 != "" and Building_Name3 in name_text and (Estate_Name in Estate_text or Estate_Name2 in Estate_text):
                        name_element.click()                      
                        return proceed_with_area_selection(driver, Build_Area, response)  

                    # 3.건물명 선처리(건물명에 아파트 있는 경우) 마지막에 아파트만 제거한다. 다음 경우의수 처리를 위해서 임시 변수에 치환하기 전에 저장한다.
                    if Building_Name4 != "" and Building_Name4 in name_text and (Estate_Name in Estate_text or Estate_Name2 in Estate_text):
                        name_element.click()                      
                        return proceed_with_area_selection(driver, Build_Area, response)                
                    
                # return proceed_with_area_selection(driver, Build_Area, response)

                response["response_code"] = "90000005"
                response["response_msg"] = f"일치하는 주소가 없습니다."
                response["data"] = [0, 0, 0, 0]
                return response
            
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 결과를 처리 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"검색 결과 처리 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response
            
    except Exception as e:
        error = str(e).split(";")[0]
        error = str(error).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {error}"
        response["data"] = [0, 0, 0, 0]
        return response

    return response


# ==========================================================================================
# 도로명 주소 검색
# ==========================================================================================
def KBland_roadnum(driver, dataloop, kwargs):
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
        Doro_No2 = kwargs.get('Doro_No2')
        if Doro_No2 == '':
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No
        else:
            Doro_Name2 = kwargs.get('Doro_Name1') + ' ' + Doro_No + '-' + Doro_No2
        Chosung = kwargs.get('Chosung1')
        Build_Area = kwargs.get('Build_Area1')


        url = "https://kbland.kr/home"
        driver.get(url)

        # 팝업창 종료
        main = driver.window_handles

        for i in main:
            if i != main[0]:
                driver.switch_to.window(i)
                driver.close()

        try:
            # 페이지 로드가 완료될 때까지 기다리기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "페이지 로드 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        
        try:
            # 1. input이 포함된 div 요소 기다리기
            input_div = WebDriverWait(driver, 10).until(
                # EC.visibility_of_element_located((By.CSS_SELECTOR, ".homeSerchBox"))
                EC.visibility_of_element_located((By.CLASS_NAME, "input-land"))
            )            
            # JavaScript로 클릭 시도
            driver.execute_script("arguments[0].click();", input_div)

            time.sleep(3)
            
            # input 요소가 나타날 때까지 기다린 후 주소 입력
            input_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control"))
            )
            input_element.send_keys(Doro_Name2)
            time.sleep(2)
            input_element.send_keys(Keys.ENTER)

            time.sleep(5)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 입력 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"주소 입력 중 예외 발생: {error}"
            response["data"] = [0, 0, 0, 0]
            return response       
        
        def parse_cost_value(text):
            text = text.replace(",", "")  # 숫자에 있는 콤마 제거
            match = re.match(r"(?:(\d+)억)?\s*(?:(\d+)만)?", text)
            if match:
                billion = int(match.group(1)) * 10**8 if match.group(1) else 0
                million = int(match.group(2)) * 10**4 if match.group(2) else 0
                return billion + million
            
            return 0

        def proceed_with_area_selection(driver):
            time.sleep(3)
            try:
                area_select_div = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".widthTypeValue"))
                )
                driver.execute_script("arguments[0].click();", area_select_div)
                time.sleep(3)

                area_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tdbold"))
                )

                time.sleep(5)
                
                # 면적
                area_data = Build_Area
                cnt = 0
                area_list = []
                for element in area_elements:
                    size = element.text
                    area_list.append(size)

                for i in range(len(area_list)):
                    cnt += 1
                    if area_data in area_list[i]:
                        area_select = driver.find_elements(By.CLASS_NAME, "tdbold")[i]
                        driver.execute_script("arguments[0].click();", area_select)
                        break
                if cnt == len(area_list):
                    response["response_code"] = "90000000"
                    response["response_msg"] = "면적을 찾을 수 없음."
                    response["data"] = [0, 0, 0, 0]
                    return response

                time.sleep(5)

                try:
                    common_value_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, ".costvalue"))
                    )
                    common_value_text = common_value_element.text.strip()
                    
                    if "시세없음" in common_value_text:  # 시세없음인 경우 0 반환
                        kb_common_value = '시세없음'
                        kb_low_value = 0
                        date_text = 0
                        print("일반가 값이 '시세없음'이므로 일반가와 하위평균가를 0으로 설정합니다.")
                    else:
                        kb_common_value = parse_cost_value(common_value_text)
                        # 하위평균가 가져오기
                        low_value_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, "//span[em[text()='하위평균가']]"))
                        )
                        low_value_text = low_value_element.text.replace("하위평균가", "").strip()
                        kb_low_value = parse_cost_value(low_value_text)

                        # 기준일 가져오기
                        date_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, "//span[@class='costdate']"))
                        )
                        date_text = date_element.text.replace("’", "").strip()
                        
                except Exception as e:
                    error = str(e).split(";")[0]
                    error = str(error).split("\n")[0]
                    response["response_code"] = "90000001"
                    response["response_msg"] = f"일반가 값을 가져오는 중 오류 발생. 오류: {error}"
                    response["data"] = [0, 0, 0, 0]
                    return response
                
                # 특정 요소를 페이지 상단으로 스크롤 이동
                element = driver.find_element(By.XPATH, "//*[@class='saleBar']")                    
                driver.execute_script("arguments[0].scrollIntoView(true);", element)

                response["response_code"] = "00000000"
                response["response_msg"] = "정상적으로 처리되었습니다."
                response["data"] = [kb_common_value, kb_low_value, 0, date_text]
                return response

            except Exception as e:
                error = str(e).split(";")[0]
                error = str(error).split("\n")[0]
                response["response_code"] = "90000001"
                response["response_msg"] = f"일반가 값을 가져오는 중 오류 발생. 오류: {error}"
                response["data"] = [0, 0, 0, 0]
                return response

        try:
            # 검색 결과 대기
            WebDriverWait(driver, 10).until(
                EC.any_of(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".item-search-poi")),  # 검색 결과 항목
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".widthTypeValue")),  # 1개일 경우 바로 면적 선택
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".nodata"))  # '검색결과가 없어요.' 메시지
                )
            )
            
            # '검색결과가 없어요.' 메시지가 있는지 확인
            if driver.find_elements(By.CSS_SELECTOR, ".nodata"):
                nodata_message = driver.find_element(By.CSS_SELECTOR, ".nodata").text.strip()
                response["response_code"] = "00000000"
                response["response_msg"] = f"검색 결과가 없습니다: {nodata_message}"
                response["data"] = [0, 0, 0, 0]
                return response

            # 검색 결과가 존재하는 경우 처리
            items = driver.find_elements(By.CSS_SELECTOR, ".item-search-poi")

            if driver.find_elements(By.CSS_SELECTOR, ".widthTypeValue"):
                return proceed_with_area_selection(driver)  # 면적 선택 진행
            
            # 검색 결과가 여러 개인 경우: .item-search-poi 리스트가 나타남
            if items:
                print(f"검색 결과가 {len(items)}개 있습니다. 리스트에서 선택을 진행합니다.")
                found_item = False  # Building_Name 찾았는지 확인하는 플래그
                for item in items:
                    name_element = item.find_element(By.CSS_SELECTOR, ".text")
                    name_text = name_element.text.strip()

                    if Building_Name in name_text:
                        name_element.click()
                        found_item = True
                        return proceed_with_area_selection(driver)

                Building_Name_Tmp = Building_Name
                Building_Name = re.sub("아파트$", "", Building_Name)

                # 1. 건물명 선처리(건물명에 아파트 있는 경우) 마지막에 아파트만 제거한다. 다음 경우의수 처리를 위해서 임시 변수에 치환하기 전에 저장한다.
                for item in items:
                    name_element = item.find_element(By.CSS_SELECTOR, ".text")
                    name_text = name_element.text.strip()

                    if Building_Name in name_text:
                        name_element.click()
                        found_item = True
                        return proceed_with_area_selection(driver)
                                                      
                # 리스트를 모두 확인했지만 Building_Name 찾지 못한 경우
                if not found_item:
                    response["response_code"] = "90000001"
                    response["response_msg"] = f"항목을 찾지 못했습니다: [건물명]"
                    response["data"] = [0, 0, 0, 0]
                    return response            

        except Exception as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"항목을 찾지 못했습니다: {error}"
            response["data"] = [0, 0, 0, 0]
            return response
        
    except Exception as e:
        error = str(e).split(";")[0]
        error = str(error).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {error}"
        response["data"] = [0, 0, 0, 0]
        return response
    
    return response
