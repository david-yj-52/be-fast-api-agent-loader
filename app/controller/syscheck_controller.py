import logging
from typing import Optional

from fastapi import APIRouter
from fastapi.params import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.config_manager import ConfigManager
from app.config.sqlite_session import db_helper
from app.constant.ap_type import AgentStatus, InterfaceSystemType
from app.dao.ln_dply_file_inf.ln_lcl_dply_file_inf_orm_service import LnDplyFileInfOrmService
from app.model.agent_loader_interface_model import LOADER_SYS_HEALTH_CHECK_REP
from app.model.cmn.ap_head_vo import generate_head_vo
from app.model.cmn.ap_interface_vo import ApInterfaceVo
from app.model.server_interface_model import SERVER_DEPLOY_FILE_REQ
from app.util.http_client import ApHttpClient
from app.util.interface_uitl import convert_vo_into_dict
from app.util.os_util import get_system_type

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/sys_check",
    tags=["health"],
)

settings = ConfigManager()


async def get_ln_dply_service(db: AsyncSession = Depends(db_helper.get_db)):
    return LnDplyFileInfOrmService(db)


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


@router.get("/deploy/check/{site_id}/{grp_nm}/{ap_nm}")
async def get_current_deploy_info(
        site_id: str, grp_nm: str, ap_nm: str, service: LnDplyFileInfOrmService = Depends(get_ln_dply_service)):
    return await service.get_deployment_info(site_id, grp_nm, ap_nm)


@router.get("/deploy/file/request")
async def fetch_deploy_file_request():
    clz = SERVER_DEPLOY_FILE_REQ
    req = ApInterfaceVo[clz](
        head=generate_head_vo(clz),
        body=clz(
            siteId=settings.SITE_ID,
            apGrpNm=settings.GRP_NAME,
            apVersion="v10.0.1",
            apNm=InterfaceSystemType.AGENT,
            userOsType=get_system_type(),
            userId=InterfaceSystemType.LOADER.value
        )
    )

    client = ApHttpClient()
    client.download_file(clz, "C:\\Users\\tspsc\\Downloads\\agent-download.zip", convert_vo_into_dict(req))
