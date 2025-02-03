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
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
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

        # 저장할 폴더 경로 지정
        folder_path = os.path.join(r"C:\python\RPA\rpa\capImg")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 현재 폴더에 존재하는 파일들에서 최대 SEQ 번호 추출
        #existing_files = os.listdir(folder_path)
        #seq_numbers = []
        
        #for file in existing_files:
        #    match = re.search(rf"{Lease_Inv_Mng_No}_(\d+)\.png", file)
        #    if match:
        #        seq_numbers.append(int(match.group(1)))

        # 최대 번호 + 1로 새로운 seq 번호 생성
        #next_seq = max(seq_numbers) + 1 if seq_numbers else 701  # 시작 번호는 701

        # 파일 경로 설정
        next_seq = "70" + Rank
        screenshot_name = f"{Lease_Inv_Mng_No}_{next_seq}.png"
        print("screenshot_name : ", screenshot_name) 
        screenshot_path = os.path.join(folder_path, screenshot_name)

        # 전체 페이지 스크린샷 저장
        try:
            full_screenshot.capture_full_page(driver, screenshot_path)
            print(f"전체 페이지 스크린샷 저장 완료: {screenshot_path}")
        except Exception as e:
            print(f"스크린샷 저장 중 오류 발생: {e}")

        time.sleep(10)

    except Exception as e:
        e = str(e).split("\n")[0]
        response["response_code"] = "90000001"
        response["response_msg"] = f"스크린샷을 실패했습니다: {e}"
        response["data"] = [0, 0, 0, 0]
        return response