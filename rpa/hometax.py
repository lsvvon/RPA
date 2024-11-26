from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options   
import urllib.request
import time
import os
BACKSPACE='/ue003'
ENTER='/ue007'
TAB='/ue004'



options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
# 자동화 메세지 옵션 제거
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)

url = "https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&menuCd=H4712090300"

driver.get(url)
time.sleep(3)  

# 본번지
# input_element = driver.find_element(By.NAME, "bmno")
# time.sleep(3)
# input_element.click()
# time.sleep(3)
# input_element.send_keys('중랑구 상봉동')

login_text_element = driver.find_element(By.CLASS_NAME, "color-red")

driver.find_element("id", "mf_wfHeader_query").send_keys("기준시가")
time.sleep(3)
driver.find_element("id", "txtExstPrlno").send_keys(Keys.ENTER)
time.sleep(3)

# '오피스텔 및 상업용건물 기준시가' 링크 클릭
link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, \"doKeyword('오피스텔 및 상업용건물 기준시가')\")]"))
)
link.click()

# 클릭 후 나타난 정보를 가져오기 위해 잠시 대기
time.sleep(2)  # 혹은 WebDriverWait 사용 가능
