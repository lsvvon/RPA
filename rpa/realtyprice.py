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

url = "https://www.realtyprice.kr/notice/main/mainBody.htm"

driver.get(url)
time.sleep(3)  


links_selector = "div.quick_menu > ul > li > a"
links = driver.find_elements(By.CSS_SELECTOR, links_selector)
print(links)
##links.click()
time.sleep(3)

