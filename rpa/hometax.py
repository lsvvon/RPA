import Hometax_module
import common_module
from selenium.common.exceptions import TimeoutException

MAX_RETRIES = 3


def main(Search_Gobun, **kwargs):
    driver = None
    try:
        driver = common_module.initialize_driver()
        if Search_Gobun == '1': # 지번검색일떄 
            response = Hometax_module.hometax_streetnum(driver, **kwargs)

        elif Search_Gobun == '2':   # 도로명검색일때
            response = Hometax_module.hometax_roadnum(driver, **kwargs)
            
        common_module.screenshot_save(driver)
        return response
    
    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    main()