import logging
import os
import shutil
import sys
import winreg
import zipfile
from pathlib import Path

from app.config.config_manager import ConfigManager

logger = logging.getLogger(__name__)
_settings = ConfigManager()


def get_base_dir() -> Path:
    local_app_data = os.environ.get('LOCALAPPDATA')

    if not local_app_data:
        local_app_data = str(Path.home() / "AppData" / "Local")

    base_dir = Path(local_app_data) / _settings.GRP_NAME / _settings.AP_NAME / _settings.AP_VERSION
    return base_dir


def get_install_path():
    """레지스트리에서 Inno Setup이 저장한 실제 설치 경로를 읽어옴"""
    try:
        # HKEY_CURRENT_USER 또는 HKEY_LOCAL_MACHINE (HKA 대응)
        reg_path = r"Software\TSHInc\TSH-AGENT-LOADER"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
            install_path, _ = winreg.QueryValueEx(key, "InstallPath")
            return Path(install_path)
    except Exception:
        # 레지스트리가 없거나 오류 시 (개발 환경 등)
        if getattr(sys, 'frozen', False):
            # 최후의 수단: 환경변수 사용
            return Path(os.environ.get('NUITKA_ONEFILE_BINARY', sys.executable)).parent
        return Path(__file__).resolve().parent.parent.parent


async def extract_file(zip_file_path: str, extract_path: str):
    try:
        logger.info(f"Extracting agent from {zip_file_path} to {extract_path}")

        # 2. 압축 해제 실행
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        old_path = os.path.join(extract_path, "main.dist")
        new_path = os.path.join(extract_path, "bin")

        # 기존에 bin 폴더가 있다면 삭제 (덮어쓰기 방지)
        if os.path.exists(new_path):
            shutil.rmtree(new_path)

        # 2. 이름 변경 (main.dist -> bin)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)

        # 3. 설치 완료 후 원본 zip 파일 삭제 (선택 사항)
        parent_dir = Path(zip_file_path).parent

        if parent_dir.exists() and parent_dir.is_dir():
            shutil.rmtree(parent_dir)
        logger.info("Installation cleanup: zip file removed.")

    except zipfile.BadZipFile:
        logger.error("Error: The downloaded file is not a valid zip file.")
    except Exception as e:
        logger.error(f"Unexpected error during extraction: {e}")


def get_exe_files(folder_path: str):
    # 1. 경로 객체 생성
    path = Path(folder_path)

    # 2. rglob(recursive glob)을 사용하여 모든 하위 폴더까지 순회하며 .exe 찾기
    # 하위 폴더 제외하고 현재 폴더만 보려면 path.glob("*.exe") 사용
    exe_files = [file.name for file in path.rglob("*.exe")]

    return exe_files
