from sqlalchemy import String, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.config.sqlite_session import Base
from app.constant.ap_type import InterfaceSystemType, UserOsType
from app.constant.table_name import LoaderTableName
from app.dao.cmn.default_model_mixin import DefaultModelMixin


class LhDplyFileInf(Base, DefaultModelMixin):
    __tablename__ = LoaderTableName.LH_LCL_DPLY_FILE_INF.value

    ap_grp_nm: Mapped[str] = mapped_column(String(40), nullable=False)
    ap_nm: Mapped[InterfaceSystemType] = mapped_column(Enum(InterfaceSystemType, native_enum=False), nullable=False)
    ap_version: Mapped[str] = mapped_column(String(40), nullable=False)
    os_typ: Mapped[UserOsType] = mapped_column(Enum(UserOsType, native_enum=False), nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)


class LnDplyFileInf(Base, DefaultModelMixin):
    __tablename__ = LoaderTableName.LN_LCL_DPLY_FILE_INF.value

    ap_grp_nm: Mapped[str] = mapped_column(String(40), nullable=False)
    ap_nm: Mapped[InterfaceSystemType] = mapped_column(Enum(InterfaceSystemType, native_enum=False), nullable=False)
    ap_version: Mapped[str] = mapped_column(String(40), nullable=False)
    os_typ: Mapped[UserOsType] = mapped_column(Enum(UserOsType, native_enum=False), nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (
        Index(
            "UK_" + LoaderTableName.LN_LCL_DPLY_FILE_INF.value + "_01",
            "site_id",
            "ap_nm",
            "ap_version"
        ),
    )

    def to_history(self) -> LhDplyFileInf:
        """Kotlin의 toHistory()와 동일한 역할"""
        # 1. 현재 객체의 필드들을 dict로 추출 (SQLAlchemy 내부 상태 필드 제외)
        excluded_fields = {'_sa_instance_state', 'obj_id'}
        data = {k: v for k, v in vars(self).items() if k not in excluded_fields}

        # 2. Lh 모델 생성 (obj_id는 Mixin의 default에 의해 자동생성됨)
        return LhDplyFileInf(
            ref_obj_id=self.obj_id,  # 현재 Ln의 ID를 ref로 전달
            **data
        )
