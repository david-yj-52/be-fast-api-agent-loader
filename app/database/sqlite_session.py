import logging
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


# 3. 모든 모델의 부모 클래스
class Base(DeclarativeBase):
    pass


class DatabaseHelper:
    def __init__(self, db_path: str):
        self.config = ConfigManager()
        self.db_url = os.path.join(db_path, self.config.SQLITE_DB_NAME)

        self.engine = self._create_engine()
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

    def _create_engine(self) -> AsyncEngine:
        return create_async_engine(self.db_url, echo=True,
                                   connect_args={"check_same_thread": False} if "sqlite" in self.db_url else {})

    async def get_db(self):
        async with self.async_session_maker() as session:
            try:
                yield session
            except Exception as e:
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()

    async def close(self):
        """엔진 종료 (lifespan에서 사용)"""
        await self.engine.dispose()


# 인스턴스화하여 다른 곳에서 공유
db_helper = DatabaseHelper()
