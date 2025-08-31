@echo off
:: 문자 인코딩을 UTF-8로 설정
chcp 65001

:: 1. Python 3.12.10이 설치되어 있는지 확인하고 없으면 설치
python --version 2>nul | findstr /i "3.12.10" >nul
if %errorlevel% neq 0 (
    echo Python 3.12.10이 설치되어 있지 않습니다. Python을 설치합니다...
    :: Python 3.12.10 다운로드 링크를 자동으로 열어줍니다.
    start https://www.python.org/downloads/release/python-31210/
    exit /b
)

:: 2. 현재 디렉토리에서 venvGer 폴더가 포함되어 있는지 확인하고, 있으면 해당 경로로 이동
set target_folder=venvGer
set found=false

:: 현재 경로에서 venvGer 폴더를 찾기
    cd..
    cd /d %cd%/Scripts

    :: 3. 가상환경 활성화
    echo 가상환경을 활성화합니다...
    start /B cmd /k "call activate && python -X utf8 ..\main.py"

:: 배치 파일 종료
pause