$nuitkaOptions = @(
    "--standalone",
#     "--onefile", -- 보안 이슈를 위한 주석
    "--mingw64",
    # --- 백그라운드 실행(nohup) 설정 ---
#     "--windows-disable-console", # CMD 콘솔창이 뜨지 않게 설정
    # --enable-cache 대신 아래 옵션을 시도하거나, 일단 제외하고 진행합니다.
    # 최신 버전이 아니면 캐시 옵션 없이도 빌드는 가능합니다.
    "--jobs=$env:NUMBER_OF_PROCESSORS", 
    "--plugin-enable=anti-bloat",
    "--include-package=uvicorn",
    "--include-package=fastapi",
    "--include-package=starlette",
    "--include-package=app",
    "--include-package=sqlalchemy",
    "--include-package=pydantic",
    "--include-package=pydantic_core",
    "--include-data-file=.env=.env",
    "--output-dir=build",
    "main.py"
)

Write-Host "🚀 Nuitka 빌드를 시작합니다..." -ForegroundColor Cyan
python -m nuitka @nuitkaOptions