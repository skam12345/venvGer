@echo off
chcp 949 >nul
setlocal

echo ==== Check to Python or Version ====
set "PY_VERSION=3.12.10"
set "PY_INSTALLER=python-%PY_VERSION%-amd64.exe"
set "PY_URL=https://www.python.org/ftp/python/%PY_VERSION%/%PY_INSTALLER%"

REM py 런처로 현재 버전 확인
set "CUR_VERSION="
for /f "tokens=2 delims= " %%a in ('py --version 2^>nul') do set "CUR_VERSION=%%a"

echo [DEBUG] CUR_VERSION="%CUR_VERSION%"

if not "%CUR_VERSION%"=="%PY_VERSION%" (
    echo Python %PY_VERSION% Need to Install. Proccessing Install...

    set "TEMP_DIR=%~dp0tmp_py_install"
    if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
    cd /d "%TEMP_DIR%"

    echo Downloading for Install File..
    powershell -Command "Invoke-WebRequest -Uri %PY_URL% -OutFile %PY_INSTALLER%"

    echo Python %PY_VERSION% 설치 중...
    %PY_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    echo ==== Completed install. Check Version ====
    py --version

    cd ..
    rd /s /q "%TEMP_DIR%"
)

@echo off
setlocal

:: 관리자 권한 확인
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo ⚠️ 관리자 권한으로 다시 실행해주세요!
    pause
    exit /b
)

:: Java 설치 여부 확인
java -version >nul 2>&1
if %errorLevel% EQU 0 (
    echo ✅ Java is already installed.
    java -version
    goto :eof
)

echo ⏳ Java not found. Installing Microsoft OpenJDK 21...

:: OpenJDK 21 설치 (무인 설치)
winget install --id Microsoft.OpenJDK.21 --exact --silent --accept-source-agreements --accept-package-agreements

:: JAVA_HOME 설정
setx -m JAVA_HOME "C:\Program Files\Microsoft\jdk-21" >nul

:: PATH에 추가
setx -m PATH "%PATH%;C:\Program Files\Microsoft\jdk-21\bin" >nul

echo ✅ Installation complete. Please open a new terminal and run:
echo     java -version

echo ==== Completed Worked ====

:: ====== 가상환경 처리 ======
set "VENV_DIR=%~dp0venvGer"

if exist "%VENV_DIR%" (
    echo Existed to Virtual Environment. %VENV_DIR%
) else (
    echo No Exist Virtual Environment Create to Virtual Environment.
    py -3.12 -m venv "%VENV_DIR%"
)

echo After available Virtual Environment Installing Package...
call "%VENV_DIR%\Scripts\activate.bat"

echo ==== Checking for Package or Installed ====
call :CheckAndInstall pyttsx3
call :CheckAndInstall speechrecognition
call :CheckAndInstall numpy
call :CheckAndInstall konlpy
call :CheckAndInstall pyaudio
call :CheckAndInstall selenium

echo ==== Completed to Package ====

:: main.py 실행 (BAT 종료되지 않고 그대로 실행됨)
start /B py E:\HobbyProject\AboutGersang\gersang-sound-helper-bot\venvGer\main.py
pause
endlocal
exit /b


:CheckAndInstall
echo Checking to Package: %1
pip show %1 >nul 2>&1
if errorlevel 1 (
    echo → %1 Need to Install.. Proccessing Install ...
    python -m pip install %1
) else (
    echo → %1 Already Installed. Passed.
)

exit /b 0