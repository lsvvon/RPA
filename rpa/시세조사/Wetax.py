import Wetax_module
from selenium.common.exceptions import TimeoutException
import common_module


def main(dataloop, collected_data):
    driver = None 

    try:
        driver = common_module.initialize_driver()
        response = Wetax_module.wetax_officetel(driver, collected_data)

        common_module.screenshot_save(driver, dataloop, collected_data)

        return response
    
    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    main()