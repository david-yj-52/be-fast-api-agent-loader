import logging
import threading
import time
from typing import Dict, Callable, Optional


class ApPolingService:
    def __init__(self):
        # 실행 중인 스레드들을 관리할 딕셔너리 {"task_name": thread_object}
        self.threads: Dict[str, threading.Thread] = {}
        self.running_status: Dict[str, bool] = {}
        self.logger = logging.getLogger("ApPolingService")

    def start_task(self, task_name: str, interval: int, do_task: Callable, on_result: Optional[Callable] = None):
        """ 특정 이름의 폴링 작업을 시작 """
        if task_name in self.threads and self.threads[task_name].is_alive():
            self.logger.warning(f"Task `{task_name}`은(는) 이미 실행 중입니다.")
            return

        self.running_status[task_name] = True
        thread = threading.Thread(
            target=self._run_loop,
            args=(task_name, interval, do_task, on_result),
            daemon=True,
            name=task_name
        )
        self.threads[task_name] = thread
        thread.start()
        self.logger.info(f"Task `{task_name}` 시작됨 (주기: {interval}초)")

    def stop_task(self, task_name: str):
        """ 특정 이름의 폴링 작어만 중지 """
        if task_name in self.running_status:
            self.running_status[task_name] = False

            # 스레드가 안전하게 종료될 때 까지 대기
            if task_name in self.threads:
                self.threads[task_name].join(timeout=1)
                del self.threads[task_name]
            del self.running_status[task_name]
            self.logger.info(f"Task `{task_name}` 중지됨")
        else:
            self.logger.warning(f"Task `{task_name}`을(를) 찾을 수 없습니다.")

    def stop_all(self):
        """모든 폴링 작업 중지"""
        names = list(self.running_status.keys())
        for name in names:
            self.stop_task(name)

    def _run_loop(self, task_name: str, interval: int, do_task: Callable, on_result: Optional[Callable]):
        """ 각 스레드에서 실행될 루프 """
        while self.running_status.get(task_name, False):
            try:
                # 1. 작업 수행 및 응답 저장
                result = do_task()
                # 2. 결과 처리 콜백이 있다면 실행
                if on_result:
                    on_result(result)

            except Exception as e:
                self.logger.warning(f"Task `{task_name}` 실행 중 오류: {e}")

            # 지정된 interval 동안 1초씩 끊어서 대기 (중지 신호에 즉각 반응하기 위함)
            for _ in range(interval):
                if not self.running_status.get(task_name, False):
                    break
                time.sleep(1)
