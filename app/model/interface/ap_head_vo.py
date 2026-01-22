from pydantic import BaseModel, Field

from app.constant.ap_type import InterfaceSystemType


class HeadVo(BaseModel):
    src: InterfaceSystemType = Field(..., description="system type message source.")
    tgt: InterfaceSystemType = Field(..., description="system type message target.")
    mid: str = Field(..., description="message id.")
    tid: str = Field(..., description="transaction id")
    enm: str = Field(..., description="event name")
