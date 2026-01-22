from enum import Enum, auto


class PollingTask(Enum):
    VERSION_CHECK = auto()
    AGENT_HEALTH_CHECK = auto()
