import Rtech1_module
from selenium.common.exceptions import TimeoutException
import common_module

MAX_RETRIES = 1


def main(Estate_Gobun,addResch,Search_Gobun, **kwargs):
    attempt = 0
    # building = 'officetel' # 아파트 or 오피스텔
    # company = 'HF' # HUG or HF
    # searchType = 'road' # 지번 or 도로명

    try:
        while attempt < MAX_RETRIES:
            driver = common_module.initialize_driver()
            try:
                if Search_Gobun == '1': # 지번검색일때
                    Rtech1_module.rtech_streetnum(driver, **kwargs)
                    if addResch == 'HF':
                        Rtech1_module.search_HF(driver)
                    elif addResch == 'HUG':
                        Rtech1_module.captcha_HUG(driver, Estate_Gobun)
                    #print(rtech_module.captcha_HUG(driver,building))
                    common_module.screenshot_save(driver)
                    print("프로그램이 정상적으로 실행되었습니다.")
                    break 
                elif Search_Gobun == '2': # 도로명검색일때
                    Rtech1_module.rtech_roadnum(driver, **kwargs)
                    if addResch == 'HF':
                        Rtech1_module.search_HF(driver)
                    elif addResch == 'HUG':
                        Rtech1_module.captcha_HUG(driver, Estate_Gobun)
                    #print(rtech_module.captcha_HUG(driver,building))
                    common_module.screenshot_save(driver)
                    print("프로그램이 정상적으로 실행되었습니다.")
                    break 

            except TimeoutException as e:
                print(f"타임아웃 발생: {e}, 재시도 중...")
                attempt += 1
                driver.quit()  # 타임아웃 발생 시 드라이버 종료 후 새로 시도
        else:
            # MAX_RETRIES에 도달한 경우
            print("최대 재시도 횟수에 도달했습니다. 프로그램 종료.")

    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    Search_Gobun = '1' # 아파트 or 오피스텔
    addResch = 'HF' # HUG or HF
    Estate_Gobun = '1' # 지번 or 도로명

    main(Estate_Gobun, addResch, Search_Gobun)