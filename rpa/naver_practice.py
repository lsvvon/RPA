from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
# 자동화 메세지 옵션 제거
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)

url = "https://naver.com"

driver.get(url)
time.sleep(3) # 사람이 입력한 것처럼 보이도록 시간 주기

# 1
# query = driver.find_element(By.ID, "query")
# # query = driver.find_element(By.NAME, "query") : 위 코드와 같은 의미
# query.send_keys("인공지능")
# time.sleep(2)

# search_btn = driver.find_element(By.CSS_SELECTOR, "#search-btn")
# search_btn.click()
# time.sleep(2)

# 2
login_text_element = driver.find_element(By.CLASS_NAME, "MyView-module__login_text___G0Dzv")
login_text = login_text_element.text
driver.find_element(By.ID, "query").send_keys(login_text)
time.sleep(2)

# driver.find_element(By.CSS_SELECTOR, "#search-btn").click()
driver.find_element(By.ID, "query").send_keys(Keys.ENTER)
time.sleep(2)

driver.save_screenshot("naver_로그인.png")
# driver.quit()
