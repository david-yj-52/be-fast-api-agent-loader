import logging
from typing import Dict, Optional

from app.config.config_manager import ConfigManager
from app.config.sqlite_session import db_helper
from app.constant.ap_type import InterfaceSystemType
from app.dao.ln_dply_file_inf.ln_lcl_dply_file_inf import LnDplyFileInf
from app.dao.ln_dply_file_inf.ln_lcl_dply_file_inf_orm_service import LnDplyFileInfOrmService
from app.model.cmn.ap_head_vo import generate_head_vo
from app.model.cmn.ap_interface_vo import ApInterfaceVo
from app.model.server_interface_model import SERVER_DEPLOY_VER_REQ, SERVER_DEPLOY_VER_REP
from app.service.deploy.agent_install_service import AgentInstallService
from app.service.deploy.agent_life_time_service import AgentLifeTimeService
from app.util.http_client import ApHttpClient
from app.util.interface_uitl import convert_vo_into_dict
from app.util.os_util import get_system_type

logger = logging.getLogger(__name__)
http_client = ApHttpClient()
settings = ConfigManager()


async def _fetch_current_dploy_version() -> Optional[LnDplyFileInf]:
    async with db_helper.async_session() as session:
        orm_service = LnDplyFileInfOrmService(session)

        current_version = await orm_service.get_deployment_info(settings.SITE_ID, settings.GRP_NAME,
                                                                InterfaceSystemType.AGENT.name)
        if not current_version:
            raise Exception(f"Cannot find deploy info. ${settings.SITE_ID}:{settings.GRP_NAME}:{settings.AP_NAME}")
        return current_version


def ask_server_deploy_version() -> ApInterfaceVo[SERVER_DEPLOY_VER_REP]:
    clz = SERVER_DEPLOY_VER_REQ
    req = ApInterfaceVo[clz](
        head=generate_head_vo(clz),
        body=clz(
            siteId=settings.SITE_ID,
            userId=InterfaceSystemType.LOADER.name,
            apGrpNm=settings.GRP_NAME,
            apNm=InterfaceSystemType.AGENT,
            userOsType=get_system_type(),
        )
    )
    response = http_client.request(clz, json=convert_vo_into_dict(req))
    return ApInterfaceVo[SERVER_DEPLOY_VER_REP].model_validate(response.json())


class AgentManager:
    def __init__(self):
        self.life_time_services: Dict[str, AgentLifeTimeService] = {}
        self.life_time_service = None
        self.install_service = None

    async def initialize(self):

        try:
            db_version_info = await _fetch_current_dploy_version()
            server_deploy_info = ask_server_deploy_version()

            server_v = str(server_deploy_info.body.apVersion)
            db_v = str(db_version_info.ap_version)
            logger.info(
                f"dbVersion vs payloadVersion {db_v} {server_v} ")

            if db_v == server_v:
                self.life_time_service = AgentLifeTimeService(str(db_version_info.file_path))
                self.life_time_service.start()
                self.life_time_services[str(db_version_info.ap_version)] = self.life_time_service

            else:
                logger.info(f"version has been changed. start update sequnce.")
                self.install_service = AgentInstallService(server_deploy_info)
                await self.install_service.start_install()

                #         // TODO 기존 agent stop & DB 삭제 및 이력 남기기
                logger.info(f"update sequnce start.")
                await AgentInstallService(server_deploy_info).start_install()
                logger.info("start run agent.")
                db_version_info = await _fetch_current_dploy_version()
                self.life_time_service = AgentLifeTimeService(str(db_version_info.file_path))
                self.life_time_service.start()
                self.life_time_services[str(db_version_info.ap_version)] = self.life_time_service

        except Exception as ex:
            logger.info(f"first install.{ex}")
            server_deploy_info = ask_server_deploy_version()
            await AgentInstallService(server_deploy_info).start_install()

            logger.info("start run agent.")
            db_version_info = await _fetch_current_dploy_version()
            self.life_time_service = AgentLifeTimeService(str(db_version_info.file_path))
            self.life_time_service.start()
            self.life_time_services[str(db_version_info.ap_version)] = self.life_time_service

    def is_agent_install_properly(self):
        """ Agent가 잘 설치되고 있고 기동 가능한 상황인지 확인 """


agent_manager = AgentManager()
