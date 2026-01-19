import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# .env 파일 로드
load_dotenv()

# DB URL 설정 (기본값: 프로젝트 루트의 note_metadata.db)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./note_metadata.db")

# 1. 비동기 엔진 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # SQL 로그 출력 (개발용)
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 2. 비동기 세션 메이커
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# 3. 모든 모델의 부모 클래스
class Base(DeclarativeBase):
    pass


# 4. FastAPI 의존성 주입용 함수
async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
