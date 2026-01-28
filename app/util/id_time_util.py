import hashlib
import subprocess
import uuid

from app.constant.ap_type import UserOsType
from app.util.os_util import get_system_type


def generate_obj_id():
    return generate_id("OBJ")


def generate_tid():
    return generate_id("TID")


def generate_id(prefix: str):
    return prefix + "-" + _generate_unique_id()


def _generate_unique_id():
    return str(uuid.uuid4())


def get_device_unique_id():
    os_type = get_system_type()
    device_id = ""

    try:
        if os_type == UserOsType.WINDOWS:
            # 메인보드 UUID
            cmd = "wmic csproduct get uuid"
            device_id = subprocess.check_output(cmd, shell=True).decode().split("\n")[1].strip()
        elif os_type == UserOsType.LINUX:
            # 시스템 머신 ID
            try:
                with open("/var/lib/dbus/machine-id", "r") as f:
                    device_id = f.read().strip()
            except:
                with open("/etc/machine-id", "r") as f:
                    device_id = f.read().strip()

        elif os_type == UserOsType.MAC:  # macOS
            # 하드웨어 UUID
            cmd = "ioreg -rd1 -c IOPlatformExpertDevice | grep IOPlatformUUID"
            output = subprocess.check_output(cmd, shell=True).decode()
            device_id = output.split('"')[-2]

    except Exception as e:
        # 최후의 보루 : MAC 주소 기반 UUID
        device_id = str(uuid.getnode())

    # 보안을 위해 한 번 해싱하여 일정한 길이의 ID로 만듦
    print(f"decoed 전 : ${device_id}")
    return hashlib.sha256(device_id.encode()).hexdigest()
