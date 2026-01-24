import logging
import os
import subprocess

import psutil

from app.config.config_manager import ConfigManager

logger = logging.getLogger(__name__)
settings = ConfigManager()


class AgentLifeTimeService:
    def __init__(self, exe_path: str):
        self.exe_path = exe_path
        self.exe_name = os.path.basename(exe_path)
        self.process = None

    def is_running(self) -> bool:
        """현재 Agent 프로세스가 실행 중인지 확인합니다."""
        # 1. 내가 직접 관리하는 핸들이 있는 경우
        if self.process and self.process.poll() is None:
            logger.info(f"Agent is running (Internal PID: {self.process.pid})")
            return True

        # 2. 핸들은 없지만 시스템에 이미 떠 있는 경우 (경로까지 비교)
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                # 이름이 일치하는지 확인
                if proc.info['name'].lower() == self.exe_name.lower():
                    # 실행 파일의 전체 경로(exe)까지 일치하는지 확인 (가장 정확)
                    if proc.info['exe'] and os.path.normpath(proc.info['exe']).lower() == os.path.normpath(
                            self.exe_path).lower():
                        logger.info(f"Agent found in system (PID: {proc.info['pid']}, Path: {proc.info['exe']})")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return False

    def start(self) -> bool:
        """Agent를 실행합니다."""
        if self.is_running():
            logger.info("Agent is already running.")
            return True

        try:
            # CREATE_NEW_PROCESS_GROUP: Loader와 별개 프로세스로 관리
            # DETACHED_PROCESS: 콘솔 창 없이 백그라운드 실행 (필요 시 선택)
            self.process = subprocess.Popen(
                [self.exe_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                shell=False
            )
            logger.info(f"Agent started (PID: {self.process.pid})")
            return True
        except Exception as e:
            logger.error(f"Failed to start Agent: {e}")
            return False

    def stop(self) -> bool:
        """실행 중인 Agent를 안전하게 종료합니다."""
        found = False
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() == self.exe_name.lower():
                    logger.info(f"Terminating Agent (PID: {proc.pid})...")
                    proc.terminate()  # Graceful shutdown 요청

                    # 종료될 때까지 최대 5초 대기
                    _, alive = psutil.wait_procs([proc], timeout=5)
                    if alive:
                        logger.warning("Agent did not terminate, killing...")
                        proc.kill()  # 강제 종료
                    found = True
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logger.error(f"Error while stopping process: {e}")

        self.process = None
        return found
