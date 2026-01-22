import platform

from app.constant.ap_type import UserOsType


def get_system_type() -> UserOsType | None:
    try:
        return UserOsType(platform.system())
    except ValueError:
        return None
