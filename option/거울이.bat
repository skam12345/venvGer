@echo off
chcp 65001 >nul
setlocal

echo ==== Python 설치 확인 시작 ====
set "PY_VERSION=3.12.10"
set "PY_INSTALLER=python-%PY_VERSION%-amd64.exe"
set "PY_URL=https://www.python.org/ftp/python/%PY_VERSION%/%PY_INSTALLER%"

REM py 런처로 현재 버전 확인
set "CUR_VERSION="
for /f "tokens=2 delims= " %%a in ('py --version 2^>nul') do set "CUR_VERSION=%%a"

echo [DEBUG] CUR_VERSION="%CUR_VERSION%"

if not "%CUR_VERSION%"=="%PY_VERSION%" (
    echo Python %PY_VERSION% 설치 필요. 설치 진행...

    set "TEMP_DIR=%~dp0tmp_py_install"
    if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
    cd /d "%TEMP_DIR%"

    echo 설치 파일 다운로드 중...
    powershell -Command "Invoke-WebRequest -Uri %PY_URL% -OutFile %PY_INSTALLER%"

    echo Python %PY_VERSION% 설치 중...
    %PY_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    echo ==== 설치 완료. 버전 확인 ====
    py --version

    cd ..
    rd /s /q "%TEMP_DIR%"
)

echo ==== 작업 완료 ====

:: ====== 가상환경 처리 ======
set "VENV_DIR=%~dp0venvGer"

if exist "%VENV_DIR%" (
    echo 가상환경이 존재합니다: %VENV_DIR%
) else (
    echo 가상환경이 없으므로 새로 만듭니다...
    py -3.12 -m venv "%VENV_DIR%"
)

echo 가상환경 활성화 후 패키지 설치...
call "%VENV_DIR%\Scripts\activate.bat"

echo ==== 패키지 확인 및 설치 ====
call :CheckAndInstall pyttsx3
call :CheckAndInstall speechrecognition
call :CheckAndInstall numpy
call :CheckAndInstall konlpy
call :CheckAndInstall pyaudio

echo ==== 패키지 설치 완료 ====

:: main.py 실행 (BAT 종료되지 않고 그대로 실행됨)
start /B python ..\main.py

pause
endlocal
exit /b


:CheckAndInstall
echo 패키지 확인 중: %1
pip show %1 >nul 2>&1
if errorlevel 1 (
    echo → %1 설치 필요. 설치 진행...
    python -m pip install %1
) else (
    echo → %1 이미 설치됨. 건너뜀.
)

exit /b 0