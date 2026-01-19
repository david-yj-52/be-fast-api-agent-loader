import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.config.config_manager import ApSettings
from app.controller.health_controller import router as health_router
from app.service.agent_version_check_service import AgentVersionCheckService
from app.util.polling_client import ApPolingService

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("LoaderMain")

settings = ApSettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # [STARTUP] 어플리케이션 기동 시 실행
    logger.info("========================================")
    logger.info("Loader Application Starting...")
    logger.info("========================================")

    # 버전 체크 서비스 시작
    version_check = AgentVersionCheckService()
    version_check.start_task()

    yield  # 서버가 기동되는 지점

    # [SHUTDOWN] 어플리케이션 중단 시 실행
    logger.info("========================================")
    logger.info("Loader Application Shutting Down...")
    logger.info("========================================")
    # 폴링 서비스 중단 등 정리 작업
    ApPolingService().stop_all()


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=settings.AP_PORT)
