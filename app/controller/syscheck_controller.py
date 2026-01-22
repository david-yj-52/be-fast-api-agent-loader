import logging
from typing import Optional

from fastapi import APIRouter
from fastapi.params import Query

from app.config.config_manager import ConfigManager
from app.constant.ap_type import AgentStatus
from app.model.interface.agent_loader_interface_model import LOADER_SYS_HEALTH_CHECK_REP
from app.model.interface.ap_head_vo import generate_head_vo
from app.model.interface.ap_interface_vo import ApInterfaceVo

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/sys_check",
    tags=["health"],
)

settings = ConfigManager()


@router.get("/health", response_model=ApInterfaceVo[LOADER_SYS_HEALTH_CHECK_REP])
async def get_loader_status(
        enm: Optional[str] = Query(None, description="Event Name")
):
    """로더의 현재 가동 상태 확인"""
    logger.info(f"enm: {enm}")
    response = ApInterfaceVo[LOADER_SYS_HEALTH_CHECK_REP](
        head=generate_head_vo(LOADER_SYS_HEALTH_CHECK_REP),
        body=LOADER_SYS_HEALTH_CHECK_REP(
            status=AgentStatus.ACTIVE,
            version=settings.AP_VERSION,
            running=True
        )
    )
    return response


@router.post("/update/check")
async def manual_update_check():
    """웹에서 즉시 업데이트 체크를 요청할 때 사용"""
    # TODO: VersionCheckService의 메서드 호출 로직 추가
    return {"message": "Manual update check initiated"}
