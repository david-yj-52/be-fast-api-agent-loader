import sys
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


class ConfigManager(BaseSettings):
    # !. env에 항목 추가 시 필드 정의 추가 필수
    GRP_NAME: str
    AP_NAME: str
    AP_VERSION: str
    AP_PORT: int

    SERVER_BE_BASE_URL: str
    SOLACE_URL: str
    SOLACE_VPN: str
    SOLACE_TOPIC: str
    AGENT_BASE_URL: str

    SQLITE_DB_NAME: str

    URI_PREFIX: str

    print(f"ENV_PATH: {ENV_PATH}")
    # .env 파일을 자동으로 읽어도록 설정 가능
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding='utf-8')
