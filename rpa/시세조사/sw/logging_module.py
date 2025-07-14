import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.DEBUG):
    """
    로거를 설정하고 반환합니다.
    
    Args:
        name (str): 로거 이름.
        log_file (str): 로그를 저장할 파일 경로.
        level (int): 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    
    Returns:
        logging.Logger: 설정된 로거 객체.
    """
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 파일 핸들러 (로그를 파일에 저장)
    handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3  # 5MB 넘으면 새로운 파일 생성
    )
    handler.setLevel(level)

    # 로그 형식
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # 핸들러 추가
    logger.addHandler(handler)

    return logger
