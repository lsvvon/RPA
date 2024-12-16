import rtech_module
from selenium.common.exceptions import TimeoutException
import common_module

MAX_RETRIES = 1
attempt = 0
building = 'officetel'
company = 'HUG'
try:
    while attempt < MAX_RETRIES:
        driver = common_module.initialize_driver()
        try:
            rtech_module.rtech_roadnum(driver)
            if company == 'HF':
                rtech_module.search_HF(driver)
            elif company == 'HUG':
                rtech_module.captcha_HUG(driver, building)
            #print(rtech_module.captcha_HUG(driver,building))
            common_module.screenshot_save(driver, "rtech_capImg")
            print("프로그램이 정상적으로 실행되었습니다.")
            break  # 성공하면 반복 종료

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