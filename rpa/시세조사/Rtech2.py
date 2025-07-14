import Rtech2_module
import common_module



def main(dataloop, collected_data):
    driver = None 

    try:
        driver = common_module.initialize_driver()
        for entry in dataloop:
            Search_Gubun = entry.get("Search_Gubun")

        if Search_Gubun == '1': # 지번검색일때
            response = Rtech2_module.rtech_app_streetnum(driver, dataloop, collected_data)
            if response["response_code"] == "00000000":
                response = Rtech2_module.captcha_APP(driver, dataloop, collected_data)

        elif Search_Gubun == '2': # 도로명검색일때
            response = Rtech2_module.rtech_app_roadnum(driver, dataloop, collected_data)
            if response["response_code"] == "00000000":
                response = Rtech2_module.captcha_APP(driver, dataloop, collected_data)

        common_module.screenshot_save(driver, dataloop, collected_data)

        return response
        
    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    main()