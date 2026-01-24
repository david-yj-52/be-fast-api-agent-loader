from typing import TypeVar, Generic

from pydantic import BaseModel

from app.model.cmn.ap_head_vo import HeadVo

T = TypeVar("T")


class ApInterfaceVo(BaseModel, Generic[T]):
    """ 공통 IVO 구조 """
    head: HeadVo
    body: T
