import os
import sys
import winreg
from pathlib import Path

from app.config.config_manager import ConfigManager

# 1. 모듈 수준에서 설정 객체 생성 (싱글톤처럼 작동)
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
