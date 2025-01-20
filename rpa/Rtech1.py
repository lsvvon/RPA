import Rtech1_module
from selenium.common.exceptions import TimeoutException
import common_module


def main(addResch, Search_Gubun, Estate_Gubun, **kwargs):
    driver = None 
    try:        
        driver = common_module.initialize_driver()

        if Search_Gubun == '1': # 지번검색일때
            response = Rtech1_module.rtech_streetnum(driver, Estate_Gubun, **kwargs)
            if not response["response_code"]:
                if addResch == 'HF':
                    response = Rtech1_module.search_HF(driver)
                elif addResch == 'HUG':
                    response = Rtech1_module.captcha_HUG(driver, Estate_Gubun, **kwargs)


        elif Search_Gubun == '2': # 도로명검색일때
            response = Rtech1_module.rtech_roadnum(driver, Estate_Gubun, **kwargs)
            if not response["response_code"]:
                if addResch == 'HF':
                    response = Rtech1_module.search_HF(driver)
                elif addResch == 'HUG':
                    response = Rtech1_module.captcha_HUG(driver, Estate_Gubun, **kwargs)
         
        common_module.screenshot_save(driver)

        
        return response
    
    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    main()