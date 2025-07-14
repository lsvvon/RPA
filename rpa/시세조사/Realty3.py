import realtyprice_module
from selenium.common.exceptions import TimeoutException
import common_module
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def main(dataloop, collected_data):
    driver = None

    try: 
        driver = common_module.initialize_driver()
        for entry in dataloop:
            Search_Gubun = entry.get("Search_Gubun")

        if Search_Gubun == '1':
            response = realtyprice_module.realtyprice_land_streetnum(driver, collected_data)

        elif Search_Gubun == '2':
            response = realtyprice_module.realtyprice_land_roadnum(driver, collected_data)

        # 특정 요소를 페이지 상단으로 스크롤 이동
        element = driver.find_element(By.XPATH, "//*[@class='searchform']")
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

        common_module.screenshot_save(driver, dataloop, collected_data)
        return response

    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    main()