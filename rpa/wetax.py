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

url = "https://www.wetax.go.kr/tcp/loi/J030401M01.do"

driver.get(url)
time.sleep(3)  

# 본번지
# input_element = driver.find_element(By.NAME, "bmno")
# time.sleep(3)
# input_element.click()
# time.sleep(3)
# input_element.send_keys('중랑구 상봉동')

login_text_element = driver.find_element(By.CLASS_NAME, "color-red")
login_text = login_text_element.text
print(login_text)
# 본번지
driver.find_element("id", "txtExstPrlno").send_keys("2255")
#time.sleep(3)
driver.find_element("id", "txtExstPrlno").send_keys(Keys.ENTER)
#time.sleep(3)
# 부번지
driver.find_element("name", "bsno").send_keys("4")
driver.find_element("name", "bsno").send_keys(Keys.ENTER)

   # '검색어 입력' 필드를 찾고 값 입력
#search_input = WebDriverWait(driver, 10).until(
#    EC.presence_of_element_located((By.ID, "txtExstPrlno"))
#)
#search_input.clear()  # 기존 값이 있을 경우 제거
#search_input.send_keys("오피스텔")  # 원하는 검색어 입력

#id 속성으로 접근
#driver.find_element_by_id('txtExstPrlno').send_keys("1234")

# 관할자치단체
select = Select(driver.find_element(By.NAME, 'ctpvCd'))
select.select_by_index(1)
time.sleep(2)

select_1 = Select(driver.find_element(By.NAME, 'sggCd'))
select_1.select_by_index(1)
time.sleep(2)

select_2 = Select(driver.find_element(By.NAME, 'stdgCd'))
select_2.select_by_index(1)
time.sleep(2)

# 기준연도
select_3 = Select(driver.find_element(By.NAME, 'aplcnYr'))
select_3.select_by_index(1)
time.sleep(2)

# 특수번지
select_4 = Select(driver.find_element(By.NAME, 'srgCd'))
select_4.select_by_index(1)
time.sleep(2)


# 검색 버튼 클릭
driver.find_element("id", "btnSrchBldsCpb").click()
# driver.find_element_by_xpath('//*[@id="btnSrchBldsCpb"]/div[7]/a[2]').click()