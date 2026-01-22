import logging
import os.path

from platformdirs import user_data_dir

from app.config.config_manager import ConfigManager
from app.database.sqlite_session import Base, db_helper
from app.service.agent_health_check_service import AgentHealthCheckService

logger = logging.getLogger(__name__)


class ServiceStartActivator():
    def __init__(self):
        self.settings = ConfigManager()

    async def doStart(self):
        # [STARTUP] 어플리케이션 기동 시 실행
        logger.info("========================================")
        logger.info("Loader Application Starting...")
        logger.info("========================================")

        logger.info("Start Polling Task.")
        self._executePollingTask()

        logger.info("Start Folders")
        self._setUpFolder()

        logger.info("Start DB setup")
        await self._setup_database()

    def _executePollingTask(self):
        # self.versionCheck = AgentVersionCheckService()
        # self.versionCheck.start_task()

        self.agent_health_check = AgentHealthCheckService()
        self.agent_health_check.start_task()

    def _setUpFolder(self):
        self.appDir = user_data_dir()
        self.baseDir = os.path.join(self.appDir, self.settings.GRP_NAME, self.settings.AP_NAME,
                                    self.settings.AP_VERSION)
        if not os.path.exists(self.baseDir):
            os.makedirs(self.baseDir)

        self.data_path = os.path.join(self.baseDir, 'data')
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        logger.info(f"apDir: {self.appDir} baseDir: {self.baseDir} dataPath: {self.data_path}")

    async def _setup_database(self):
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    service = ServiceStartActivator()
    service._setUpFolder()
