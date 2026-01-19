import logging
import os.path

from platformdirs import user_data_dir

from app.config.config_manager import ConfigManager
from app.service.agent_version_check_service import AgentVersionCheckService

logger = logging.getLogger(__name__)


class ServiceStartActivator():
    def __init__(self):
        self.settings = ConfigManager()

    def doStart(self):
        # [STARTUP] 어플리케이션 기동 시 실행
        logger.info("========================================")
        logger.info("Loader Application Starting...")
        logger.info("========================================")

        logger.info("Start Polling Task.")
        self._executePollingTask()

        logger.info("Start Folders")
        self._setUpFolder()

    def _executePollingTask(self):
        self.versionCheck = AgentVersionCheckService()
        self.versionCheck.start_task()

    def _setUpFolder(self):
        self.appDir = user_data_dir()
        self.baseDir = os.path.join(self.appDir, self.settings.GRP_NAME, self.settings.AP_NAME,
                                    self.settings.AP_VERSION)
        if not os.path.exists(self.baseDir):
            os.makedirs(self.baseDir)

        self.dbPath = os.path.join(self.baseDir, self.settings.SQLITE_DB_NAME)
        logger.info(f"apDir: {self.appDir} baseDir: {self.baseDir} dbPath: {self.dbPath}")

    # def _setUpDatabase(self):


if __name__ == '__main__':
    service = ServiceStartActivator()
    service._setUpFolder()
