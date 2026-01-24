import logging
import os

from platformdirs import user_data_dir

from app.config.config_manager import ConfigManager
from app.config.sqlite_session import db_helper
from app.constant.ap_type import InterfaceSystemType
from app.dao.ln_dply_file_inf.ln_lcl_dply_file_inf import LnDplyFileInf
from app.dao.ln_dply_file_inf.ln_lcl_dply_file_inf_orm_service import LnDplyFileInfOrmService
from app.model.cmn.ap_head_vo import generate_head_vo
from app.model.cmn.ap_interface_vo import ApInterfaceVo
from app.model.server_interface_model import SERVER_DEPLOY_VER_REP, SERVER_DEPLOY_FILE_REQ
from app.util.http_client import ApHttpClient
from app.util.interface_uitl import convert_vo_into_dict
from app.util.os_util import get_system_type
from app.util.path_util import extract_file, get_exe_files

logger = logging.getLogger(__name__)
settings = ConfigManager()
http_client = ApHttpClient(settings.SERVER_BE_BASE_URL)


def _generate_agent_install_path(deploy_inf: SERVER_DEPLOY_VER_REP):
    ap_grp_nm = deploy_inf.apGrpNm
    ap_nm = deploy_inf.apNm
    ap_version = deploy_inf.apVersion
    return os.path.join(user_data_dir(), ap_grp_nm, ap_nm.value, ap_version)


async def _fetch_deploy_file(ap_version: str, file_path: str):
    clz = SERVER_DEPLOY_FILE_REQ
    req = ApInterfaceVo[clz](
        head=generate_head_vo(clz),
        body=clz(
            siteId=settings.SITE_ID,
            apGrpNm=settings.GRP_NAME,
            apVersion=ap_version,
            apNm=InterfaceSystemType.AGENT,
            userOsType=get_system_type(),
            userId=InterfaceSystemType.LOADER.value
        )
    )

    http_client.download_file(clz, file_path, convert_vo_into_dict(req))


class AgentInstallService:
    def __init__(self, ivo: ApInterfaceVo[SERVER_DEPLOY_VER_REP]):
        self.ivo = ivo
        self.body = ivo.body
        self.base_path = None
        self.tmp_path = None
        self.agent_bin_path = None

    async def start_install(self):
        if not self.body.apVersion:
            raise Exception("Nothing register at server side.")
        self.make_agent_folders()

        target_zip_file = os.path.join(self.tmp_path, f"agent-download-{self.body.apVersion}.zip")
        await _fetch_deploy_file(self.body.apVersion, target_zip_file)

        await extract_file(target_zip_file, self.base_path)

        self.agent_bin_path = os.path.join(self.base_path, "bin")
        exe_file_list = get_exe_files(self.agent_bin_path)
        if (len(exe_file_list) > 1): raise Exception(f"exe file over 1. ${exe_file_list}")

        exe_file_name = exe_file_list[0]

        await self.register_new_agent_into_db(os.path.join(self.agent_bin_path, exe_file_name))

    async def register_new_agent_into_db(self, exe_file_path: str):

        entity = LnDplyFileInf(
            ap_grp_nm=self.body.apGrpNm,
            ap_nm=self.body.apNm,
            ap_version=self.body.apVersion,
            os_typ=get_system_type(),
            file_path=exe_file_path,
            tid=self.ivo.head.tid,
            evnt_nm=self.body.__class__.__name__,
            crt_user_id=InterfaceSystemType.LOADER.value,
            mdfy_user_id=InterfaceSystemType.LOADER.value
        )

        async with db_helper.async_session() as session:
            orm_service = LnDplyFileInfOrmService(session)
            await orm_service.add_new_deployment(entity)

    def make_agent_folders(self):

        base_path = _generate_agent_install_path(self.body)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        self.base_path = base_path

        data_path = os.path.join(base_path, "data")
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        install_tmp_path = os.path.join(base_path, "tmp")
        if not os.path.exists(install_tmp_path):
            os.makedirs(install_tmp_path)
        self.tmp_path = install_tmp_path
