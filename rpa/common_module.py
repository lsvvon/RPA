from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import full_screenshot
import os
import time

def initialize_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
    return webdriver.Chrome(options=options)

def screenshot_save(driver):
    # 저장할 폴더 경로 지정
    folder_path = os.path.join(r"C:\python\RPA\rpa\capImg")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    unique_number = '5000000000'
    # 파일 경로 설정
    screenshot_name = f"{unique_number}_901.png"
    screenshot_path = os.path.join(folder_path, screenshot_name)

    # 전체 페이지 스크린샷 저장
    full_screenshot.capture_full_page(driver, screenshot_path)
    print(f"전체 페이지 스크린샷 저장 완료: {screenshot_path}")

    time.sleep(10)
