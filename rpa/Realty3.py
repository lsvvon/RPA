import realtyprice_module
from selenium.common.exceptions import TimeoutException
import common_module



def main(Search_Gubun, **kwargs):
    driver = None

    try: 
        driver = common_module.initialize_driver()
        if Search_Gubun == '1':
            response = realtyprice_module.realtyprice_land_streetnum(driver, **kwargs)

        elif Search_Gubun == '2':
            response = realtyprice_module.realtyprice_land_roadnum(driver, **kwargs)

        common_module.screenshot_save(driver)
        return response

    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    main()