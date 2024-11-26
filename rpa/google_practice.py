from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# 크롬 웹드라이버를 자동으로 설치 및 설정


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 구글 지도 접속하기
driver.get("https://www.google.com/maps/")

# 검색창에 "카페" 입력하기
searchbox = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input#searchboxinput"))
)
searchbox.send_keys("카페")
# 검색버튼 누르기
searchbutton = driver.find_element(By.CSS_SELECTOR, "button#searchbox-searchbutton")
searchbutton.click()

# CSV 파일 열기 (쓰기 모드)
with open("cafe_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["가게 이름", "평점", "주소"])
    for i in range(999):
        # 시간 지연
        time.sleep(3)
       # 가게 리스트가 로드될 때까지 기다리기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.section-result-content"))
        )

        stores = driver.find_elements(By.CSS_SELECTOR, "div.section-result-content")
        print(stores)
        if not stores:
            print("더 이상 가게 정보가 없습니다.")
            break

        for s in stores:
            try:
                title = s.find_element(By.CSS_SELECTOR, "h3.section-result-title").text
            except:
                title = "가게 이름 없음"

            try:
                score = s.find_element(By.CSS_SELECTOR, "span.cards-rating-score").text
            except:
                score = "평점없음"

            try:
                addr = s.find_element(By.CSS_SELECTOR, "span.section-result-location").text
            except:
                addr = "주소 없음"

            print(title, "/", score, "/", addr)
            writer.writerow([title, score, addr])

        try:
            nextpage = driver.find_element(By.CSS_SELECTOR, "button#n7lv7yjyC35__section-pagination-button-next")
            nextpage.click()
        except:
            print("데이터 수집 완료.")
            break

driver.close()
