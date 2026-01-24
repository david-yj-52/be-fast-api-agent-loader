import platform

from app.constant.ap_type import UserOsType


def get_system_type() -> UserOsType | None:
    try:
        return UserOsType(platform.system())
    except ValueError:
        return None


if __name__ == '__main__':
    print(get_system_type().name)
    print(get_system_type().value)
