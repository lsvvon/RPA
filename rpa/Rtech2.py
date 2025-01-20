import Rtech2_module
import common_module



def main(Search_Gobun, **kwargs):
    try:
        driver = common_module.initialize_driver()

        if Search_Gobun == '1': # 지번검색일때
            response = Rtech2_module.rtech_app_streetnum(driver, **kwargs)
            if not response["response_code"]:
                response = Rtech2_module.captcha_APP(driver, **kwargs)
                print("response2", response)

        elif Search_Gobun == '2': # 도로명검색일때
            response = Rtech2_module.rtech_app_roadnum(driver, **kwargs)
            if not response["response_code"]:
                response = Rtech2_module.captcha_APP(driver, **kwargs)
                print("response2", response)

        common_module.screenshot_save(driver)

        return response
    
    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    main()