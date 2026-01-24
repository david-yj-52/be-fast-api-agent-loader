from typing import ClassVar

from pydantic import BaseModel, Field

from app.constant.ap_type import AgentStatus, HttpRequestType, InterfaceSystemType


class AGENT_SYS_HEALTH_CHECK_REQ(BaseModel):
    SRC: ClassVar[InterfaceSystemType] = InterfaceSystemType.LOADER
    TGT: ClassVar[InterfaceSystemType] = InterfaceSystemType.AGENT
    URI: ClassVar[str] = "/sys_check/health"
    METHOD: ClassVar[str] = HttpRequestType.GET.name

    data: str = Field(default=None, description="request without payload")


class AGENT_SYS_HEALTH_CHECK_REP(BaseModel):
    SRC: ClassVar[InterfaceSystemType] = InterfaceSystemType.AGENT
    TGT: ClassVar[InterfaceSystemType] = InterfaceSystemType.LOADER

    status: AgentStatus = Field(..., description="agent status")
    version: str
    path: str = Field(..., description="system runtime path.",
                      examples=[
                          'C:\\workspace\\tsh\\boilerplate\\be\\be-fast-api-agent\\build\\main.dist\\app\\controller\\syscheck_controller.py'])


class LOADER_SYS_HEALTH_CHECK_REQ(BaseModel):
    SRC: ClassVar[InterfaceSystemType] = InterfaceSystemType.AGENT
    TGT: ClassVar[InterfaceSystemType] = InterfaceSystemType.LOADER
    URI: ClassVar[str] = "/sys_check/health"
    METHOD: ClassVar[str] = HttpRequestType.GET.name


class LOADER_SYS_HEALTH_CHECK_REP(BaseModel):
    SRC: ClassVar[InterfaceSystemType] = InterfaceSystemType.LOADER
    TGT: ClassVar[InterfaceSystemType] = InterfaceSystemType.AGENT

    status: AgentStatus = Field(..., description="loader status")
    version: str
    running: bool
