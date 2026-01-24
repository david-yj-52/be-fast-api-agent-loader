import logging

from app.config.config_manager import ConfigManager
from app.config.sqlite_session import db_helper
from app.dao.ln_dply_file_inf.ln_lcl_dply_file_inf_orm_service import LnDplyFileInfOrmService

logger = logging.getLogger(__name__)
settings = ConfigManager()


async def _fetch_current_dploy_version():
    async with db_helper.async_session() as session:
        orm_service = LnDplyFileInfOrmService(session)

        current_version = await orm_service.get_deployment_info(settings.SITE_ID, settings.GRP_NAME,
                                                                settings.AP_NAME)
        if not current_version:
            raise Exception(f"Cannot find deploy info. ${settings.SITE_ID}:{settings.GRP_NAME}:{settings.AP_NAME}")
        return current_version


class AgentLifetimeManageService:
    #  def __init__(self):
    #      self.process = "AAA"
    #
    # def is_running(self) -> bool:
    #     """ 현재 Agent 프로세스가 실행 중인지 확인 합니다."""
    #     if self.process and self.process.poll() is None:
    #         return True
    #
    #
    #  def is_agent_install_properly(self):
    #         """ Agent가 잘 설치되고 있고 기동 가능한 상황인지 확인 """
    #
    #  def start_agent(self):
    #
    #  def stop_agent(self):

    pass
