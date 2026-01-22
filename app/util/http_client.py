import logging
from typing import Optional, Dict, TypeVar, Type

import requests
import urllib3.util.retry
from pydantic import BaseModel
from requests.adapters import HTTPAdapter

from app.config.config_manager import ConfigManager
from app.constant.ap_type import HttpRequestType

logger = logging.getLogger(__name__)
T = TypeVar('T', bound=BaseModel)


class ApHttpClient:
    def __init__(self, base_url: str = "", timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.session = self._generate_session(max_retries)

    def request(self, ivo_class: Type[T], params: Optional[Dict] = None, data: Optional[Dict] = None,
                json: Optional[Dict] = None, headers: Optional[Dict] = None,
                stream: bool = False) -> requests.Response:

        # GET 요청일 때 enm 쿼리 파라미터 추가
        if ivo_class.METHOD == HttpRequestType.GET.name:
            # 기존 params에 enm 추가
            if params is None:
                params = {}
            params['enm'] = ivo_class.__name__

        return self._request(ivo_class.METHOD, ivo_class.URI, params, data, json, headers, stream)

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None,
                 json: Optional[Dict] = None, headers: Optional[Dict] = None,
                 stream: bool = False) -> requests.Response:
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout,
                stream=stream
            )

            # 전체 URL 출력 (쿼리 파라미터 포함)
            logger.debug(f"[Request] {method} {response.url}")

            response.raise_for_status()  # 4xx, 5xx 에러 시 예외 발생
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"[HTTP Error] {method} {url} : {e}")
            raise e

    def download_file(self, url: str, save_path: str):
        """ 대용량 파일(에이전트 패치 파일 등) 다운로드 용 """
        with self.request("GET", url, stream=True) as response:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return save_path

    def _generate_session(self, max_retires: int) -> requests.Session:
        session = requests.Session()
        retry_strategy = self._retry_strategy_session(max_retires)
        adapter = HTTPAdapter(max_retries=retry_strategy)

        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _retry_strategy_session(self, max_retires: int) -> urllib3.util.retry.Retry:
        return urllib3.util.retry.Retry(
            total=max_retires,
            backoff_factor=1,  # 재시도 간격: 1s, 2s, 4s...
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "TRUE"]

        )


if __name__ == '__main__':
    settings = ConfigManager()
    httpClient = ApHttpClient(base_url=settings.SERVER_BE_BASE_URL)
    try:
        response = httpClient.request("GET", "/health")
        print(response.json())
    except Exception as e:
        print(e)
