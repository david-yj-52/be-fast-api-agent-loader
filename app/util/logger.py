import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.util.path_util import get_install_path


def setup_logger():
    # 1. 경로 결정
    if getattr(sys, 'frozen', False):
        # 실행 파일(.exe) 환경: 무조건 우리가 정의한 AppData 고정 경로 사용
        # Nuitka가 sys.executable을 어디로 잡든 상관없이 get_base_dir()이 우선순위를 가집니다.
        base_path = get_install_path()
    else:
        # 로컬 개발 환경: 기존처럼 프로젝트 루트 경로 사용
        base_path = Path(__file__).resolve().parent.parent.parent

    print(f"DEBUG: Executable Path: {sys.executable}")
    print(f"DEBUG: Base Path: {base_path}")

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
