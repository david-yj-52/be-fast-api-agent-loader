from typing import Optional, ClassVar, Dict

from pydantic import BaseModel, Field

from app.constant.ap_type import InterfaceSystemType, HttpRequestType, UserOsType
from app.model.cmn.ap_head_vo import generate_head_vo
from app.model.cmn.ap_interface_vo import ApInterfaceVo


class ServerBodyCommon(BaseModel):
    siteId: str
    userId: str


class ServerReqBodyCommon(ServerBodyCommon):
    URI: ClassVar[str]
    METHOD: ClassVar[str]
    SRC: ClassVar[InterfaceSystemType] = InterfaceSystemType.LOADER
    TGT: ClassVar[InterfaceSystemType] = InterfaceSystemType.SERVER

    def get_params(self) -> Dict[str, any]:
        """인스턴스 필드를 딕셔너리로 변환"""
        # PARAM이 정의되어 있으면 해당 키만 사용
        if hasattr(self.__class__, 'PARAM'):
            return {key: getattr(self, key) for key in self.__class__.PARAM.keys()}
        # 없으면 모든 필드 사용
        return self.model_dump()


class SERVER_SYS_HEALTH_CHECK_REQ(ServerReqBodyCommon):
    URI: ClassVar[str] = "/sys_check/health"
    METHOD: ClassVar[str] = HttpRequestType.GET.name

    data: Optional[str] = Field(default=None, description="request without payload")


class SERVER_SYS_HEALTH_CHECK_REP(ServerBodyCommon):
    message: str
    timestamp: str = Field(..., examples=["2026-01-23T05:02:20.31944973"])


class SERVER_DEPLOY_FILE_REQ(ServerReqBodyCommon):
    URI: ClassVar[str] = "/deploy/file"
    METHOD: ClassVar[str] = HttpRequestType.GET.name

    apGrpNm: str = Field(..., description="AP Group Name")
    apNm: InterfaceSystemType = Field(..., description="AP Name")
    apVersion: str = Field(..., description="AP Version")
    userOsType: UserOsType = Field(..., description="user os type")


class SERVER_DEPLOY_VER_REQ(ServerReqBodyCommon):
    URI: ClassVar[str] = "/deploy/version"
    METHOD: ClassVar[str] = HttpRequestType.GET.name

    apGrpNm: str = Field(..., description="AP Group Name")
    apNm: InterfaceSystemType = Field(..., description="AP Name")
    userOsType: UserOsType = Field(..., description="user os type")


class SERVER_DEPLOY_VER_REP(ServerBodyCommon):
    URI: ClassVar[str] = "/deploy/version"
    METHOD: ClassVar[str] = HttpRequestType.GET.name

    apGrpNm: str = Field(..., description="AP Group Name")
    apNm: InterfaceSystemType = Field(..., description="AP Name")
    apVersion: str = Field(..., description="AP Version")
    userOsType: UserOsType = Field(..., description="user os type")


class PARAM_SAMPLE(ServerReqBodyCommon):
    URI: ClassVar[str] = "/deploy/file"
    METHOD: ClassVar[str] = HttpRequestType.GET.name
    PARAM: ClassVar[Dict[str, str]] = {"siteId": "", "apGrpNm": "", "apNm": ""}

    apGrpNm: str = Field(..., description="AP Group Name")
    apNm: InterfaceSystemType = Field(..., description="AP Name")


if __name__ == '__main__':
    req = PARAM_SAMPLE(
        apGrpNm="MyGroup",
        apNm=InterfaceSystemType.AGENT,
        siteId="siteId",
        userId="userId",
    )

    # 파라미터 확인
    print(req.get_params())

    req = ApInterfaceVo[SERVER_DEPLOY_VER_REQ](
        head=generate_head_vo(SERVER_DEPLOY_VER_REQ),
        body=SERVER_DEPLOY_VER_REQ(
            userId="userId",
            siteId="siteId",
            apGrpNm="MyGroup",
            apNm=InterfaceSystemType.AGENT,
            userOsType=UserOsType.WINDOWS

        )
    )

    print(
        req.model_dump_json()
    )
