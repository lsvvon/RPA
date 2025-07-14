from logging_module import setup_logger
import logging

# 로거 설정
app_logger = setup_logger('AppLogger', 'application.log', level=logging.DEBUG)

# 예제 로그 기록
app_logger.debug("Debugging the application.")
app_logger.info("Application started.")
app_logger.warning("This is a warning.")
app_logger.error("An error occurred.")
app_logger.critical("Critical issue!")
