from typing import Optional

from pydantic import BaseModel, Field

from app.constant.ap_type import InterfaceSystemType
from app.model.interface.ApInterfaceVo import ApInterfaceVo
from app.model.interface.common.ApHeadVo import HeadVo


class ServerBodyCommon(BaseModel):
    userId: str


class ServerSysHealthCheckReq(ServerBodyCommon):
    data: Optional[str] = Field(default=None, description="request without payload")


class ServerSysHealthCheckRep(ServerBodyCommon):
    message: str
    timestamp: str = Field(..., examples=["2026-01-23T05:02:20.31944973"])


if __name__ == '__main__':
    req = ApInterfaceVo[ServerSysHealthCheckReq](
        head=HeadVo(
            src=InterfaceSystemType.LOADER,
            tgt=InterfaceSystemType.SERVER,
            tid="ABSCEFG",
            mid="Message Key",
            enm=ServerSysHealthCheckReq.__name__
        ),
        body=ServerSysHealthCheckReq(
            userId="userId",
        )
    )

    print(
        req.model_dump_json()
    )
