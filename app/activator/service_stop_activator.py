import logging

from app.util.polling_client import ApPolingService

logger = logging.getLogger(__name__)


class ServiceStopActivator():

    def doStop(self):
        logger.info("========================================")
        logger.info("Loader Application Shutting Down...")
        logger.info("========================================")

        self.pollingService = ApPolingService()
        self.pollingService.stop_all()
