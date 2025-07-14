import Hometax_module
import common_module
from selenium.common.exceptions import TimeoutException

MAX_RETRIES = 3


def main(dataloop, collected_data):
    driver = None

    try:
        driver = common_module.initialize_driver()
        for entry in dataloop:
            Search_Gubun = entry.get("Search_Gubun") 
        
        if Search_Gubun == '1': # 지번검색일떄 
            response = Hometax_module.hometax_streetnum(driver, collected_data)

        elif Search_Gubun == '2':   # 도로명검색일때
            response = Hometax_module.hometax_roadnum(driver, collected_data)
            
        common_module.screenshot_save(driver, dataloop, collected_data)
        return response
   
    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    main()