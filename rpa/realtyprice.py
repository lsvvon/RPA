import realtyprice_module
from selenium.common.exceptions import TimeoutException
import common_module

MAX_RETRIES = 1


def main():
    attempt = 0
    driver = None 
    searchType = 'street' # 지번 or 도로명
    building = 'land' # 공동주택 or 개별주택 or 토지

    try:
        while attempt < MAX_RETRIES:
            driver = common_module.initialize_driver()
            try:
                if building =='apt': # 공동주택일때
                    if searchType == 'street':
                        realtyprice_module.realtyprice_apt_streetnum(driver)
                        common_module.screenshot_save(driver, "realtyprice_capImg")
                        print("공동주택/지번검색 완료")
                        break  
                    elif searchType == 'road':
                        realtyprice_module.realtyprice_apt_roadnum(driver)
                        common_module.screenshot_save(driver, "realtyprice_capImg")
                        print("공동주택/도로명검색 완료")
                        break                  
                elif building == 'individual': # 개별주택일때
                    if searchType == 'street':
                        realtyprice_module.realtyprice_individual_streetnum(driver)
                        common_module.screenshot_save(driver, "realtyprice_capImg")
                        print("개별단독주택/지번검색 완료")
                        break  
                    elif searchType == 'road':
                        realtyprice_module.realtyprice_individual_roadnum(driver)
                        common_module.screenshot_save(driver, "realtyprice_capImg")
                        print("개별단독주택/도로명검색 완료")
                        break   
                elif building == 'land':
                    if searchType == 'street':
                        realtyprice_module.realtyprice_land_streetnum(driver)
                        common_module.screenshot_save(driver, "realtyprice_capImg")
                        print("개별공시지가/지번검색 완료")
                        break  
                    elif searchType == 'road':
                        realtyprice_module.realtyprice_land_roadnum(driver)
                        common_module.screenshot_save(driver, "realtyprice_capImg")
                        print("개별공시지가/도로명검색 완료")
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
    main()