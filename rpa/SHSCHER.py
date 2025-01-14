from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import re

# 지번 검색
def KBland_streetnum(driver):
    url = "https://bizssl.shinhanci.com:8443/SHSCHER/asp/RPA/test.asp"
    driver.get(url)

    # 팝업창 종료
    main = driver.window_handles

    for i in main:
        if i != main[0]:
            driver.switch_to.window(i)
            driver.close()

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # 1. input이 포함된 div 요소 기다리기
    input_div = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".homeSerchBox"))
    )
    
    # JavaScript로 클릭 시도
    driver.execute_script("arguments[0].click();", input_div)

    time.sleep(3)

    item_name = '서초대우아이빌'
    
    # input 요소가 나타날 때까지 기다린 후 주소 입력
    input_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control"))
    )
    input_element.send_keys("상봉동 495")
    input_element.send_keys(Keys.ENTER)

    time.sleep(3)

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

            area_data = '59.02'  # 임의의 면적값
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
                print(f"'{area_data}' 면적을 찾을 수 없었습니다.")
                raise TimeoutException("면적 값을 찾을 수 없습니다.")  # 타임아웃 예외 발생

            time.sleep(5)

            try:
                common_value_element = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".costvalue"))
                )
                common_value_text = common_value_element.text.strip()
                
                if "시세없음" in common_value_text:  # 시세없음인 경우 0 반환
                    kb_common_value = 0
                    kb_low_value = 0
                    print("일반가 값이 '시세없음'이므로 일반가와 하위평균가를 0으로 설정합니다.")
                else:
                    kb_common_value = parse_cost_value(common_value_text)
                    # 하위평균가 가져오기
                    low_value_element = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[em[text()='하위평균가']]"))
                    )
                    low_value_text = low_value_element.text.replace("하위평균가", "").strip()
                    kb_low_value = parse_cost_value(low_value_text)
            except Exception as e:
                print(f"일반가 값을 가져오는 중 오류 발생. 오류: {e}")

            time.sleep(3)      

            print(f"하위평균가: {kb_low_value}, 일반가: {kb_common_value}")
            return kb_low_value, kb_common_value

        except Exception as e:
            print(f"면적 선택 작업 중 오류 발생: {e}")
            return None

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
            print(f"검색 결과가 없습니다: {nodata_message}")
            return None

        # 검색 결과가 존재하는 경우 처리
        items = driver.find_elements(By.CSS_SELECTOR, ".item-search-poi")

        if driver.find_elements(By.CSS_SELECTOR, ".widthTypeValue"):
            print("검색 결과가 1개만 존재하여 바로 면적 선택으로 진행합니다.")
            return proceed_with_area_selection(driver)  # 면적 선택 진행
        
         # 검색 결과가 여러 개인 경우: .item-search-poi 리스트가 나타남
        items = driver.find_elements(By.CSS_SELECTOR, ".item-search-poi")
        if items:
            print(f"검색 결과가 {len(items)}개 있습니다. 리스트에서 선택을 진행합니다.")
            for item in items:
                name_element = item.find_element(By.CSS_SELECTOR, ".text")
                name_text = name_element.text.strip()

                if item_name in name_text:
                    print(f"'{item_name}' 항목을 찾았습니다.")
                    name_element.click()
                    return proceed_with_area_selection(driver)
            print(f"'{item_name}'로 바로 다음 작업으로 넘어갑니다.")
            return proceed_with_area_selection(driver)

    except Exception as e:
        print(f"항목을 찾지 못했습니다. {e}")
        return None


# 도로명 주소 검색
def KBland_roadnum(driver):
    url = "https://kbland.kr/map?xy=37.5205559,126.9265729,17"
    driver.get(url)

    # 팝업창 종료
    main = driver.window_handles

    for i in main:
        if i != main[0]:
            driver.switch_to.window(i)
            driver.close()

    # 페이지 로드가 완료될 때까지 기다리기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # 1. input이 포함된 div 요소 기다리기
    input_div = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".homeSerchBox"))
    )
    
    # JavaScript로 클릭 시도
    driver.execute_script("arguments[0].click();", input_div)

    time.sleep(3)

    item_name = '아아'
    
    # input 요소가 나타날 때까지 기다린 후 주소 입력
    input_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-control"))
    )
    input_element.send_keys("상봉동 동부아파트")
    input_element.send_keys(Keys.ENTER)

    time.sleep(3)

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

            area_data = '21.90'  # 임의의 면적값
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
                print(f"'{area_data}' 면적을 찾을 수 없었습니다.")
                raise TimeoutException("면적 값을 찾을 수 없습니다.")  # 타임아웃 예외 발생

            time.sleep(5)

            try:
                common_value_element = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".costvalue"))
                )
                common_value_text = common_value_element.text.strip()
                
                if "시세없음" in common_value_text:  # 시세없음인 경우 0 반환
                    kb_common_value = 0
                    kb_low_value = 0
                    print("일반가 값이 '시세없음'이므로 일반가와 하위평균가를 0으로 설정합니다.")
                else:
                    kb_common_value = parse_cost_value(common_value_text)
                    # 하위평균가 가져오기
                    low_value_element = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[em[text()='하위평균가']]"))
                    )
                    low_value_text = low_value_element.text.replace("하위평균가", "").strip()
                    kb_low_value = parse_cost_value(low_value_text)
            except Exception as e:
                print(f"일반가 값을 가져오는 중 오류 발생. 오류: {e}")

            time.sleep(3)      

            print(f"하위평균가: {kb_low_value}, 일반가: {kb_common_value}")
            return kb_low_value, kb_common_value

        except Exception as e:
            print(f"면적 선택 작업 중 오류 발생: {e}")
            return None

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
            print(f"검색 결과가 없습니다: {nodata_message}")
            return None

        # 검색 결과가 존재하는 경우 처리
        items = driver.find_elements(By.CSS_SELECTOR, ".item-search-poi")

        if driver.find_elements(By.CSS_SELECTOR, ".widthTypeValue"):
            print("검색 결과가 1개만 존재하여 바로 면적 선택으로 진행합니다.")
            return proceed_with_area_selection(driver)  # 면적 선택 진행
        
         # 검색 결과가 여러 개인 경우: .item-search-poi 리스트가 나타남
        items = driver.find_elements(By.CSS_SELECTOR, ".item-search-poi")
        if items:
            print(f"검색 결과가 {len(items)}개 있습니다. 리스트에서 선택을 진행합니다.")
            found_item = False  # item_name을 찾았는지 확인하는 플래그
            for item in items:
                name_element = item.find_element(By.CSS_SELECTOR, ".text")
                name_text = name_element.text.strip()

                if item_name in name_text:
                    print(f"'{item_name}' 항목을 찾았습니다.")
                    name_element.click()
                    found_item = True
                    return proceed_with_area_selection(driver)
                
            # 리스트를 모두 확인했지만 item_name을 찾지 못한 경우
            if not found_item:
                print(f"'{item_name}' 항목을 찾지 못했습니다. 프로그램을 종료합니다.")
                return None  # 프로그램 종료

    except Exception as e:
        print(f"항목을 찾지 못했습니다. {e}")
        return None