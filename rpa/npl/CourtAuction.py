import CourtAuction_module
from selenium.common.exceptions import TimeoutException
import common_module



def main(dataloop, collected_data):
    driver = None
    
    try:
        driver = common_module.initialize_driver()
        response = CourtAuction_module.search_auction(driver, collected_data)

        return response

    finally:
        if driver:
            driver.quit()  # 드라이버가 존재하면 종료
        print("프로그램 종료.")

if __name__ == "__main__":
    dataloop = [{
        "Ticker": "Etax",
        "Rank": "01",
    }]
    
    collected_data = {
        "Court": "안산지원",
        "CaseYear": "2023",
        "CaseNo": "63037"
    }

    result = main(dataloop, collected_data)
    print("결과:", result)