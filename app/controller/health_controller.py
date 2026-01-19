from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/")
async def get_loader_status():
    """로더의 현재 가동 상태 확인"""
    return {
        "status": "active",
        "version": "1.0.0",
        "agent_running": True  # 나중에 실제 상태와 연동
    }


@router.post("/update/check")
async def manual_update_check():
    """웹에서 즉시 업데이트 체크를 요청할 때 사용"""
    # TODO: VersionCheckService의 메서드 호출 로직 추가
    return {"message": "Manual update check initiated"}
