import logging
from functools import partial

from app.config.config_manager import ConfigManager
from app.constant.ap_type import InterfaceSystemType
from app.constant.task_name import PollingTask
from app.model.cmn.ap_head_vo import generate_head_vo
from app.model.cmn.ap_interface_vo import ApInterfaceVo
from app.model.server_interface_model import SERVER_DEPLOY_VER_REQ
from app.util.http_client import ApHttpClient
from app.util.interface_uitl import convert_vo_into_dict
from app.util.os_util import get_system_type
from app.util.polling_client import ApPolingService

logger = logging.getLogger(__name__)


class AgentVersionCheckService:
    def __init__(self):
        self.task_name = PollingTask.VERSION_CHECK.name
        self.interval = 60
        self.polling_service = ApPolingService()
        self.apSettings = ConfigManager()

    def start_task(self):
        httpCliet = ApHttpClient(self.apSettings.SERVER_BE_BASE_URL)

        clz = SERVER_DEPLOY_VER_REQ
        payload = ApInterfaceVo[clz](
            head=generate_head_vo(clz),
            body=clz(
                siteId=self.apSettings.SITE_ID,
                userId=InterfaceSystemType.LOADER.name,
                apGrpNm=self.apSettings.GRP_NAME,
                apNm=InterfaceSystemType.AGENT,
                userOsType=get_system_type()

            )
        )
        logger.info(f"payload:{payload.model_dump(mode='json')}")

        do_task = partial(httpCliet.request, ivo_class=clz, json=convert_vo_into_dict(payload))
        on_result = self.handle_response

        self.polling_service.start_task(task_name=self.task_name, interval=self.interval, do_task=do_task,
                                        on_result=on_result)
        logger.info("Agent Version Check Service Started.")

    def stop_task(self):
        self.polling_service.stop_task(task_name=self.task_name)
        logger.info(f"Agent Version Check Service Stopped. task:{self.task_name}")

    def handle_response(self, response):
        """ Polling 결과를 처리 """
        if response and response.status_code == 200:
            data = response.json()
            logger.info(f"result:{data}")
        else:
            logger.error("서버 응답이 올바르지 않습니다.")
