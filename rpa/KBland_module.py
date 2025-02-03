from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import re

# 지번 검색
def KBland_streetnum(driver, dataloop, kwargs):
    response = {
        "response_code": None,
        "response_msg": None,
        "data": None,
    }

    for entry in dataloop:
        Estate_Gubun = entry.get("Estate_Gubun") 

    if Estate_Gubun == '1':
        Estate_Name = '아파트'
    elif Estate_Gubun == '4':
        Estate_Name = '오피스텔'

    try:
        # 주소 값 가져오기
        Sido = kwargs.get('Sido1')
        Sigungu = kwargs.get('Sigungu1')
        Ridong = kwargs.get('Ridong1')
        Jibun_No1 = kwargs.get('Jibun_No1')
        Jibun_No2 = kwargs.get('Jibun_No2')
        Building_Name = kwargs.get('Building_Name1')
        Build_Area = kwargs.get('Build_Area1')

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
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "페이지 로드 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response

        # 주소 입력 영역
        try:
            input_div = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".homeSerchBox"))
            )
            driver.execute_script("arguments[0].click();", input_div)

            time.sleep(3)

            input_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control"))
            )

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
            time.sleep(5)
        

        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 입력 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"주소 입력 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response

        def parse_cost_value(text):
            match = re.match(r"(\d+)억\s*([\d,]*)", text)
            if match:
                billion = int(match.group(1)) * 10**8
                million = int(match.group(2).replace(",", "")) * 10**4 if match.group(2) else 0
                return billion + million
            return 0
            
        def proceed_with_area_selection(driver, Build_Area, response):
            try:
                time.sleep(3)
                area_select_div = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".widthTypeValue"))
                )
                driver.execute_script("arguments[0].click();", area_select_div)
                time.sleep(3)

                area_elements = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tdbold"))
                )
                area_list = [element.text for element in area_elements]
                cnt = 0

                for i in range(len(area_list)):
                    cnt += 1
                    if Build_Area in area_list[i]:
                        area_select = driver.find_elements(By.CLASS_NAME, "tdbold")[i]
                        driver.execute_script("arguments[0].click();", area_select)
                        break

                if cnt == len(area_list):
                    response["response_code"] = "90000000"
                    response["response_msg"] = "면적을 찾을 수 없음."
                    response["data"] = [0, 0, 0, 0]
                    return response
                
                time.sleep(3)
                common_value_element = WebDriverWait(driver, 20).until(
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
                    low_value_element = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[em[text()='하위평균가']]"))
                    )
                    low_value_text = low_value_element.text.replace("하위평균가", "").strip()
                    kb_low_value = parse_cost_value(low_value_text)
                    # 기준일 가져오기
                    date_element = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[@class='costdate']"))
                    )
                    date_text = date_element.text.replace("’", "").strip()

                response["response_code"] = "00000000"
                response["response_msg"] = "정상적으로 처리되었습니다."
                response["data"] = [kb_common_value, kb_low_value, 0, date_text]            
                return response

            except TimeoutException:
                response["response_code"] = "90000000"
                response["response_msg"] = "예상치 못한 오류 발생."
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
                response["response_code"] = "90000000"
                response["response_msg"] = f"검색 결과가 없습니다: {nodata_message}"
                response["data"] = [0, 0, 0, 0]
                return response

            items = driver.find_elements(By.CSS_SELECTOR, ".item-search-poi")

            if driver.find_elements(By.CSS_SELECTOR, ".widthTypeValue"):
                return proceed_with_area_selection(driver, Build_Area, response)

            if items:
                for item in items:
                    name_element = item.find_element(By.CSS_SELECTOR, ".text")
                    name_text = name_element.text.strip()

                    if Building_Name in name_text:
                        name_element.click()
                        return proceed_with_area_selection(driver, Build_Area, response)

                return proceed_with_area_selection(driver, Build_Area, response)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 결과를 처리 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"검색 결과 처리 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
            
    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response

    return response

# 도로명 주소 검색
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
        Doro_Name = kwargs.get('Doro_Name1')
        Chosung = kwargs.get('Chosung1')
        Build_Area = kwargs.get('Build_Area1')

        url = "https://kbland.kr/map?xy=37.5205559,126.9265729,17"
        driver.get(url)

        # 팝업창 종료
        main = driver.window_handles

        for i in main:
            if i != main[0]:
                driver.switch_to.window(i)
                driver.close()

        try:
            # 페이지 로드가 완료될 때까지 기다리기
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "페이지 로드 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        
        try:
            # 1. input이 포함된 div 요소 기다리기
            input_div = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".homeSerchBox"))
            )
            
            # JavaScript로 클릭 시도
            driver.execute_script("arguments[0].click();", input_div)

            time.sleep(3)
            
            # input 요소가 나타날 때까지 기다린 후 주소 입력
            input_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control"))
            )
            input_element.send_keys(Doro_Name)
            input_element.send_keys(Keys.ENTER)

            time.sleep(3)
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "주소 입력 중 타임아웃 발생."
            response["data"] = [0, 0, 0, 0]
            return response
        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"주소 입력 중 예외 발생: {e}"
            response["data"] = [0, 0, 0, 0]
            return response       

        def parse_cost_value(text):
            match = re.match(r"(\d+)억\s*([\d,]*)", text)
            if match:
                billion = int(match.group(1)) * 10**8
                million = int(match.group(2).replace(",", "")) * 10**4 if match.group(2) else 0
                return billion + million
            return 0

        def proceed_with_area_selection(driver):
            time.sleep(3)
            try:
                area_select_div = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".widthTypeValue"))
                )
                driver.execute_script("arguments[0].click();", area_select_div)
                time.sleep(3)

                area_elements = WebDriverWait(driver, 20).until(
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
                    common_value_element = WebDriverWait(driver, 20).until(
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
                        low_value_element = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "//span[em[text()='하위평균가']]"))
                        )
                        low_value_text = low_value_element.text.replace("하위평균가", "").strip()
                        kb_low_value = parse_cost_value(low_value_text)

                        # 기준일 가져오기
                        date_element = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "//span[@class='costdate']"))
                        )
                        date_text = date_element.text.replace("’", "").strip()
                        
                except Exception as e:
                    e = str(e).split("\n")[0]
                    response["response_code"] = "90000001"
                    response["response_msg"] = f"일반가 값을 가져오는 중 오류 발생. 오류: {e}"
                    response["data"] = [0, 0, 0, 0]
                    return response
                time.sleep(3)      
                response["response_code"] = "00000000"
                response["response_msg"] = "정상적으로 처리되었습니다."
                response["data"] = [kb_common_value, kb_low_value, 0, date_text]
                return response


            except Exception as e:
                e = str(e).split("\n")[0]
                response["response_code"] = "90000001"
                response["response_msg"] = f"일반가 값을 가져오는 중 오류 발생. 오류: {e}"
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
                response["response_code"] = "90000001"
                response["response_msg"] = f"검색 결과가 없습니다: {nodata_message}"
                response["data"] = [0, 0, 0, 0]
                return response

            # 검색 결과가 존재하는 경우 처리
            items = driver.find_elements(By.CSS_SELECTOR, ".item-search-poi")

            if driver.find_elements(By.CSS_SELECTOR, ".widthTypeValue"):
                print("검색 결과가 1개만 존재하여 바로 면적 선택으로 진행합니다.")
                return proceed_with_area_selection(driver)  # 면적 선택 진행
            
            # 검색 결과가 여러 개인 경우: .item-search-poi 리스트가 나타남
            items = driver.find_elements(By.CSS_SELECTOR, ".item-search-poi")
            if items:
                print(f"검색 결과가 {len(items)}개 있습니다. 리스트에서 선택을 진행합니다.")
                found_item = False  # Building_Name 찾았는지 확인하는 플래그
                for item in items:
                    name_element = item.find_element(By.CSS_SELECTOR, ".text")
                    name_text = name_element.text.strip()

                    if Building_Name in name_text:
                        print(f"'{Building_Name}' 항목을 찾았습니다.")
                        name_element.click()
                        found_item = True
                        return proceed_with_area_selection(driver)
                    
                # 리스트를 모두 확인했지만 Building_Name 찾지 못한 경우
                if not found_item:
                    response["response_code"] = "90000001"
                    response["response_msg"] = f"항목을 찾지 못했습니다: {e}"
                    response["data"] = [0, 0, 0, 0]
                    return response

        except Exception as e:
            e = str(e).split("\n")[0]
            response["response_code"] = "90000001"
            response["response_msg"] = f"항목을 찾지 못했습니다: {e}"
            response["data"] = [0, 0, 0, 0]
            return response
        
    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"예상치 못한 오류 발생: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    
    return response
