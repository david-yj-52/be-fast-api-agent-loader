# import logging
# import os
# import shutil
# import subprocess
#
# import psutil
#
#
# class AgentManager:
#     def __init__(self, exe_path: str):
#         self.exe_path = exe_path
#         self.exe_name = os.path.basename(exe_path)
#         self.process = None
#         self.logger = logging.getLogger("AgentManager")
#
#     def is_running(self) -> bool:
#         """현재 Agent 프로세스가 실행 중인지 확인합니다."""
#         if self.process and self.process.poll() is None:
#             return True
#
#         # PID가 유실되었을 경우를 대비해 프로세스 이름으로 한 번 더 확인
#         for proc in psutil.process_iter(['name']):
#             try:
#                 if proc.info['name'].lower() == self.exe_name.lower():
#                     return True
#             except (psutil.NoSuchProcess, psutil.AccessDenied):
#                 continue
#         return False
#
#     def start(self) -> bool:
#         """Agent를 실행합니다."""
#         if self.is_running():
#             self.logger.info("Agent is already running.")
#             return True
#
#         try:
#             # CREATE_NEW_PROCESS_GROUP: Loader와 별개 프로세스로 관리
#             # DETACHED_PROCESS: 콘솔 창 없이 백그라운드 실행 (필요 시 선택)
#             self.process = subprocess.Popen(
#                 [self.exe_path],
#                 creationflags=subprocess.CREATE_NEW_CONSOLE,
#                 shell=False
#             )
#             self.logger.info(f"Agent started (PID: {self.process.pid})")
#             return True
#         except Exception as e:
#             self.logger.error(f"Failed to start Agent: {e}")
#             return False
#
#     def stop(self) -> bool:
#         """실행 중인 Agent를 안전하게 종료합니다."""
#         found = False
#         for proc in psutil.process_iter(['name']):
#             try:
#                 if proc.info['name'].lower() == self.exe_name.lower():
#                     self.logger.info(f"Terminating Agent (PID: {proc.pid})...")
#                     proc.terminate()  # Graceful shutdown 요청
#
#                     # 종료될 때까지 최대 5초 대기
#                     _, alive = psutil.wait_procs([proc], timeout=5)
#                     if alive:
#                         self.logger.warning("Agent did not terminate, killing...")
#                         proc.kill()  # 강제 종료
#                     found = True
#             except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
#                 self.logger.error(f"Error while stopping process: {e}")
#
#         self.process = None
#         return found
#
#     def update_executable(self, new_exe_data: bytes) -> bool:
#         """Agent 파일을 교체합니다. 실행 중이면 중지 후 교체합니다."""
#         try:
#             # 1. 기존 에이전트 중지
#             self.stop()
#
#             # 2. 백업 생성
#             backup_path = self.exe_path + ".bak"
#             if os.path.exists(self.exe_path):
#                 shutil.copy2(self.exe_path, backup_path)
#
#             # 3. 새 파일 쓰기
#             with open(self.exe_path, "wb") as f:
#                 f.write(new_exe_data)
#
#             self.logger.info("Agent executable updated successfully.")
#             return True
#         except Exception as e:
#             self.logger.error(f"Update failed: {e}. Rolling back...")
#             self.rollback()
#             return False
#
#     def rollback(self):
#         """백업 파일로 복구합니다."""
#         backup_path = self.exe_path + ".bak"
#         if os.path.exists(backup_path):
#             shutil.move(backup_path, self.exe_path)
#             self.logger.info("Rollback completed.")
