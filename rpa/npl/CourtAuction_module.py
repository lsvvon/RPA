from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def search_auction(driver, kwargs):
    response = {
        "response_code": None,
        "response_msg": None,
        "data": None,
    }

    try:
        # 주소 값 가져오기
        Court = kwargs.get('Court')
        CaseYear = kwargs.get('CaseYear')
        CaseNo = kwargs.get('CaseNo')

        url = "https://www.courtauction.go.kr/pgj/index.on?w2xPath=/pgj/ui/pgj100/PGJ159M00.xml"
        driver.get(url)

        time.sleep(5)
            
        # 현재 창 정보
        # main_window = driver.current_window_handle

        # # 팝업 창 닫기 (모든 팝업 창을 닫고 메인 창으로 돌아오기)
        # for window in driver.window_handles:
        #     if window != main_window:
        #         driver.switch_to.window(window)
        #         driver.close()
                
        # # Switch to iframe
        # iframe = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        # )
        # driver.switch_to.frame(iframe)

        try:
            # 법원 선택
            court_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mf_wfm_mainFrame_sbx_auctnCsSrchCortOfc"))
            )
            Select(court_select).select_by_visible_text(Court)
            time.sleep(1)
        except NoSuchElementException as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            response["response_code"] = "90000002"
            response["response_msg"] = f"법원 select 요소를 찾을 수 없습니다. {error}"
            response["data"] = [0, 0, 0, 0]
            return response 
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "법원 select 요소 타임아웃."
            response["data"] = [0, 0, 0, 0]
            return response  
        
        try:
            # 사건년도 선택
            year_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mf_wfm_mainFrame_sbx_auctnCsSrchCsYear"))
            )
            Select(year_select).select_by_visible_text(CaseYear)
            time.sleep(1)
        except NoSuchElementException as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            response["response_code"] = "90000002"
            response["response_msg"] = f"사건년도 select 요소를 찾을 수 없습니다. {error}"
            response["data"] = [0, 0, 0, 0]
            return response 
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "사건년도 select 요소 타임아웃."
            response["data"] = [0, 0, 0, 0]
            return response  
        
        try:
            # 타경
            case_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mf_wfm_mainFrame_ibx_auctnCsSrchCsNo"))
            )
            case_input.clear()
            case_input.send_keys(CaseNo)
            time.sleep(1)

        except NoSuchElementException as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            response["response_code"] = "90000002"
            response["response_msg"] = f"타경 select 요소를 찾을 수 없습니다. {error}"
            response["data"] = [0, 0, 0, 0]
            return response 
        except TimeoutException:
            response["response_code"] = "90000000"
            response["response_msg"] = "타경 select 요소 타임아웃."
            response["data"] = [0, 0, 0, 0]
            return response    
        
        try:
            # 검색 버튼 클릭
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "mf_wfm_mainFrame_btn_auctnCsSrchBtn"))
            )
            search_button.click()
            time.sleep(3)  # 검색 결과 로딩 대기

        except NoSuchElementException as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            response["response_code"] = "90000002"
            response["response_msg"] = f"검색 버튼 요소를 찾을 수 없습니다. {error}"
            response["data"] = [0, 0, 0, 0]
            return response
        except TimeoutException as e:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 버튼 클릭 타임아웃."
            response["data"] = [0, 0, 0, 0]
            return response 
        
        # 경매조건 값 확인
        try:
            # 법원명(span) 가져오기
            court_span = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mf_wfm_mainFrame_spn_cortOfcNm"))
            )
            court_text = court_span.text.strip()
            # 사건번호(span) 가져오기
            case_span = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mf_wfm_mainFrame_spn_userCsNo"))
            )
            case_text = case_span.text.strip()
            # 두 값 비교
            if court_text == Court and case_text == CaseYear + ' 타경' + CaseNo:
                print("두 값이 모두 일치함. 다음 단계로 진행합니다.")
            else:
                print("일치하지 않음. 넘어가지 않음.")
                response["response_code"] = "90000003"
                response["response_msg"] = f"사건번호 일치 실패"
                response["data"] = [0, 0, 0, 0]
                return response
            
        except Exception as e:
            print("오류 발생:", e)
                
        try:
            status_span = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mf_wfm_mainFrame_spn_csBasDtsUltmtRslt"))
            )
            status_text = status_span.text.strip()

            # 종국결과가 "미종국"일 경우 기일내역 탭 클릭
            if status_text == "미종국":
                # "기일내역" 탭 클릭
                tab_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "mf_wfm_mainFrame_tac_srchRsltDvs_tab_tabs2_tabHTML"))
                )
                driver.execute_script("arguments[0].click();", tab_element)
                time.sleep(2)
            
            # 종국결과가 "종국"이면 종국일자 값 가져오기
            elif status_text == "종국":
                end_date_span = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "mf_wfm_mainFrame_spn_csBasDtsUltmtYmd"))
                )
                end_date = end_date_span.text.strip()
                response["response_code"] = "00000000"
                response["response_msg"] = f"종국결과가 종국이므로 종국일자 값 가져옴"
                response["data"] = end_date
                return 


        except Exception as e:
            response["response_code"] = "90000003"
            response["response_msg"] = f"기일내역 탭 클릭 실패: {str(e).splitlines()[0]}"
            response["data"] = [0, 0, 0, 0]
            return response

        
        try:
            # 기일내역 테이블 행 전체 로드
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.grid_body_row"))
            )

            result_data = []  # 전체 행의 데이터를 담을 리스트

            for row in rows:
                tds = row.find_elements(By.TAG_NAME, "td")
                
                if len(tds) >= 7:
                    기일일시 = tds[2].text.strip()
                    기일종류 = tds[3].text.strip()
                    기일장소 = tds[4].text.strip()
                    최저매각가격 = tds[5].text.strip()
                    기일결과 = tds[6].text.strip()
                    
                    result_data.append({
                        "기일일시": 기일일시,
                        "기일종류": 기일종류,
                        "기일장소": 기일장소,
                        "최저매각가격": 최저매각가격,
                        "기일결과": 기일결과
                    })

            if result_data:
                response["response_code"] = "00000000"
                response["response_msg"] = "정상적으로 처리되었습니다."
                response["data"] = result_data
            else:
                raise Exception("데이터를 가진 유효한 row가 없습니다.")
            
        except NoSuchElementException as e:
            error = str(e).split(";")[0]
            error = str(error).split("\n")[0]
            response["response_code"] = "90000002"
            response["response_msg"] = f"건물시가표준액 요소 찾을 수 없습니다. {error}"
            response["data"] = [0, 0, 0, 0]
            return response
        except TimeoutException as e:
            response["response_code"] = "90000000"
            response["response_msg"] = "검색 결과가 존재하지 않습니다.[건물시가표준액]"
            response["data"] = [0, 0, 0, 0]
            return response 
    
    except Exception as e:
        error = str(e).split(";")[0]
        error = str(error).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"프로세스 실행 중 알 수 없는 오류 발생: {error}"
        response["data"] = [0, 0, 0, 0]
        return response
    
    return response
    




    

