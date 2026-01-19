import logging
from functools import partial

from app.config.config_manager import ApSettings
from app.constant.task_name import PollingTask
from app.util.http_client import ApHttpClient
from app.util.polling_client import ApPolingService


class AgentVersionCheckService:
    def __init__(self):
        self.task_name = PollingTask.VERSION_CHECK.name
        self.interval = 60
        self.polling_service = ApPolingService()
        self.logger = logging.getLogger("AgentVersionCheckService")
        self.apSettings = ApSettings()

    def start_task(self):
        httpCliet = ApHttpClient(self.apSettings.SERVER_BE_BASE_URL)

        do_task = partial(httpCliet.request, "GET", "/health")

        self.polling_service.start_task(task_name=self.task_name, interval=self.interval, do_task=do_task)
        logging.info("Agent Version Check Service Started.")

    def stop_task(self):
        self.polling_service.stop_task(task_name=self.task_name)
        logging.info("Agent Version Check Service Stopped.")
