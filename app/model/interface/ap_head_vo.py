import uuid
from typing import Optional, Type, TypeVar

from pydantic import BaseModel, Field

from app.constant.ap_type import InterfaceSystemType

T = TypeVar('T', bound=BaseModel)


class HeadVo(BaseModel):
    src: InterfaceSystemType = Field(..., description="system type message source.")
    tgt: InterfaceSystemType = Field(..., description="system type message target.")
    mid: str = Field(..., description="message id.")
    tid: str = Field(..., description="transaction id")
    enm: str = Field(..., description="event name")


def generate_head_vo(ivo_class: Type[T], tid: Optional[str] = None) -> HeadVo:
    head = HeadVo(
        src=ivo_class.SRC,
        tgt=ivo_class.TGT,
        mid=str(uuid.uuid4()),
        tid=tid if tid else str(uuid.uuid4()),
        enm=ivo_class.__name__
    )
    return head
