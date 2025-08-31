@echo off
chcp 65001 > 

set "TARGET_DIR=%~dp0venvGer"

echo ====Checking to Update ====
cd /d "%TARGET_DIR%"
git fetch
for /f %%i in ('git rev-list HEAD...origin/main --count') do set COUNT=%%i
if "%COUNT%"=="0" (
    echo → No Exist Update Latest Status.
) else (
    echo → Exist to Update. Proccessing Pull...
    git pull origin main
)