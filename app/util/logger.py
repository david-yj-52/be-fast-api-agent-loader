import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger():
    # 1. 실행 파일(.exe) 또는 스크립트 위치 찾기
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).resolve().parent.parent.parent  # app/util 폴더 기준 상위로 이동

    # 2. 로그 디렉토리 생성
    log_dir = base_path / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "app.log"

    # 3. 포맷 설정
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 4. 핸들러 설정 (파일 및 콘솔)
    # RotatingFileHandler: 파일이 5MB 넘으면 최대 5개까지 백업하며 새로 생성
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    # basicConfig 대신 root_logger를 직접 제어
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 기존 핸들러 초기화 (혹시 모를 중복 방지)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 우리가 정의한 포맷과 핸들러 추가
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger
