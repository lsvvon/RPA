import hometax_module
import common_module
from selenium.common.exceptions import TimeoutException

MAX_RETRIES = 1


def main():
    attempt = 0
    driver = None
    searchType = 'street'
    try:
        while attempt < MAX_RETRIES:
            driver = common_module.initialize_driver()
            try:
                if searchType == 'street':
                    result = hometax_module.hometax_streetnum(driver)
                    print(result)
                    common_module.screenshot_save(driver, "hometax_capimg")
                    break  # 성공하면 반복 종료
                elif searchType == 'road':
                    result = hometax_module.hometax_roadnum(driver)
                    print(result)
                    common_module.screenshot_save(driver, "hometax_capimg")
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