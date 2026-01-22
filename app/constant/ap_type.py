from enum import Enum


class UserOsType(Enum):
    WINDOWS = "Windows"
    MAC = "Darwin"
    LINUX = "Linux"


class AgentStatus(Enum):
    ACTIVE = "Active"
    STOLE = "Stole"


class InterfaceSystemType(Enum):
    AGENT = "Agent"
    LOADER = "Loader"
    SERVER = "Server"
