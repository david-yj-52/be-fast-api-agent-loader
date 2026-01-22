# import logging
#
# logger = logging.getLogger(__name__)
#
#
# class AgentLifetimeManageService:
#     def __init__(self):
#         self.process = None
#
#    def is_running(self) -> bool:
#        """ 현재 Agent 프로세스가 실행 중인지 확인 합니다."""
#        if self.process and self.process.poll() is None:
#            return True
