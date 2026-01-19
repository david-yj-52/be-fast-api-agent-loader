import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


# 1. 사용 상태 코드 정의 (USABLE: 활성, UNUSABLE: 삭제/비활성)
class UseStatEnum(str, Enum):
    USABLE = "USABLE"
    UNUSABLE = "UNUSABLE"


# 2. 공통 컬럼 믹스인
class DefaultModelMixin:
    # 기본 키 (UUID 문자열)
    obj_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # 상태 관리 (Sync 로직의 핵심)
    use_stat_cd: Mapped[UseStatEnum] = mapped_column(
        String(20),
        default=UseStatEnum.USABLE
    )

    # 작성자 정보
    crt_user_id: Mapped[str] = mapped_column(String(50), nullable=True)
    mdfy_user_id: Mapped[str] = mapped_column(String(50), nullable=True)

    # 시간 정보 (자동 갱신)
    crt_dt: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
    )
    mdfy_dt: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    )

    # 비고 및 공통 속성
    rsn_cd: Mapped[str] = mapped_column(String(50), nullable=True)  # 사유 코드
    trns_cm: Mapped[str] = mapped_column(String(2000), nullable=True)  # 전달 주석
