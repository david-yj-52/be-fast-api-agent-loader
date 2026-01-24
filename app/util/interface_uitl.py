from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


def convert_vo_into_dict(vo: T) -> dict[str, Any]:
    return vo.model_dump(mode='json')
