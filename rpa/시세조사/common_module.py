from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import full_screenshot
import os
import re
import time

def initialize_driver():
    options = Options()    
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)    
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    return webdriver.Chrome(options=options)

def screenshot_save(driver, dataloop, kwargs):
    response = {
        "response_code": None,
        "response_msg": None,
        "data": None,
    }
        
    try:
        Lease_Inv_Mng_No = kwargs.get('Lease_Inv_Mng_No1')
       
        for entry in dataloop:
            Rank = entry.get("Rank") 

        # # 저장할 폴더 경로 지정
        # folder_path = os.path.join(r"C:\python\RPA\rpa\capImg")
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)

        # 경로 생성 (이미 존재하면 생성 안 함) 
        folder_path = os.path.join(r"C:\python\RPA\rpa\capImg")
        os.makedirs(folder_path, exist_ok=True)  # `exist_ok=True`로 디렉토리가 있을 경우 예외를 발생시키지 않음  불필요한 체크를 방지할 수 있습니다.  

        # 파일 경로 설정
        next_seq = "70" + Rank
        screenshot_name = f"{Lease_Inv_Mng_No}_{next_seq}.jpg"
        print("screenshot_name : ", screenshot_name) 
        screenshot_path = os.path.join(folder_path, screenshot_name)

        # 창 크기 조정 추가
        # try:
        #     driver.maximize_window()  # 창을 최대화
        #     time.sleep(1) 
        #     driver.set_window_rect(0, 0, 1280, 1024)  # 창 크기 강제 조정
        # except Exception as e:
        #     print(f"창 크기 변경 중 오류 발생: {e}")

        # 전체 페이지 스크린샷 저장
        try:
            # time.sleep(2)
            full_screenshot.capture_full_page(driver, screenshot_path)
            print(f"전체 페이지 스크린샷 저장 완료: {screenshot_path}")
        except Exception as e:
            print(f"스크린샷 저장 중 오류 발생: {e}")

        time.sleep(1)

    except Exception as e:
        e = str(e).split(";")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"스크린샷을 실패했습니다: {e}"
        response["data"] = [0, 0, 0, 0]
        return response
    

