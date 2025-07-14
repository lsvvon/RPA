import KBland_module
import common_module
from selenium.webdriver.common.by import By
import time

def main(dataloop, collected_data):
    driver = None
        
    try:
        driver = common_module.initialize_driver()
        for entry in dataloop:
            Search_Gubun = entry.get("Search_Gubun") 
        
        if Search_Gubun == '1': # 지번검색일때            
            response = KBland_module.KBland_streetnum(driver, dataloop, collected_data)
        elif Search_Gubun == '2':   # 도로명검색일때
            response = KBland_module.KBland_roadnum(driver, dataloop, collected_data)           

        common_module.screenshot_save(driver, dataloop, collected_data)

        return response
   
    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    main()