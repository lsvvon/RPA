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
    return webdriver.Chrome(options=options)

def screenshot_save(driver,site):
    # 저장할 폴더 경로 지정
    folder_path = os.path.join(r"C:\python\RPA\rpa\capImg", site)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 파일 경로 설정
    screenshot_path = os.path.join(folder_path, "full_page_screenshot.png")
    full_screenshot.capture_full_page(driver, screenshot_path)
    print(f"전체 페이지 스크린샷 저장 완료: {screenshot_path}")

    time.sleep(10)
