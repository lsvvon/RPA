from selenium.webdriver.chrome.options import Options
import common_module
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

# 드라이버 초기화
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = common_module.initialize_driver()
url = "https://bizssl.shinhanci.co.kr/SHSCHER/Asp/RPA/CA_RPA_Condition.asp"
driver.get(url)
#print("RPA_main.driver: ", driver)
time.sleep(5)


# 파일 업로드 요소 찾기
file_input = driver.find_element(By.ID, "txtFile")  # ID를 사용해 찾기
time.sleep(3)

file_name = "5000000000_901.png"  # 업로드하려는 파일 이름
folder_path = r"C:\python\RPA\rpa\capImg"  # capImg 폴더의 절대 경로
file_path = os.path.join(folder_path, file_name)

# 파일이 실제로 존재하는지 확인
if os.path.exists(file_path):
    print(f"File exists at: {file_path}")
else:
    print("File does not exist. Check the path.")

file_input.send_keys(file_path)

# uploaded_image = driver.find_element(By.ID, "uploadedImagePreview")
# uploaded_image_src = uploaded_image.get_attribute("src")
# print(f"Uploaded image URL: {uploaded_image_src}")

# if "expected_image_name" in uploaded_image_src:
#     print("Correct image uploaded.")
# else:
#     print("Incorrect image uploaded.")

time.sleep(3)

# 필요한 경우 제출 버튼 클릭
# submit_button = driver.find_element(By.ID, "submitButton")
# submit_button.click()

# 브라우저 종료
