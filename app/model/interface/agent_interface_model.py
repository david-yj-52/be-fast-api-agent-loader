from typing import ClassVar

from pydantic import BaseModel, Field

from app.constant.ap_type import AgentStatus, HttpRequestType


class AgentSysHealthCheckReq(BaseModel):
    URI: ClassVar[str] = "/health"
    METHOD: ClassVar[str] = HttpRequestType.GET.name

    data: str = Field(..., description="request without payload")


class AgentSysHealthCheckRep(BaseModel):
    status: AgentStatus = Field(..., description="agent status")
    version: str
    path: str = Field(..., description="system runtime path.",
                      examples=[
                          'C:\\workspace\\tsh\\boilerplate\\be\\be-fast-api-agent\\build\\main.dist\\app\\controller\\syscheck_controller.py'])
