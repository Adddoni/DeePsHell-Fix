:: External commands
if "%~1"=="status_zapret" (
    call :test_service zapret soft
    call :tcp_enable
    exit /b
)

if "%~1"=="load_game_filter" (
    call :game_switch_status
    exit /b
)


if "%1"=="admin" (
    echo Started with admin rights
) else (
    echo Requesting admin rights...
    powershell -Command "Start-Process 'cmd.exe' -ArgumentList '/c \"\"%~f0\" admin\"' -Verb RunAs"
    exit
)


:: MENU ================================
setlocal EnableDelayedExpansion
:menu
cls
call :game_switch_status

set "menu_choice=null"
echo =========  v!LOCAL_VERSION!  =========
echo 6. Switch Game Filter (%GameFilterStatus%)
echo 0. Exit
set /p menu_choice=Enter choice: 

if "%menu_choice%"=="3" goto service_status
if "%menu_choice%"=="6" goto game_switch
if "%menu_choice%"=="0" exit /b
goto menu

:: GAME SWITCH ========================
:game_switch_status
chcp 437 > nul

set "gameFlagFile=%~dp0bin\game_filter.enabled"

if exist "%gameFlagFile%" (
    set "GameFilterStatus=enabled"
    set "GameFilter=1024-65535"
) else (
    set "GameFilterStatus=disabled"
    set "GameFilter=12"
)
exit /b


:game_switch
chcp 437 > nul
cls

if not exist "%gameFlagFile%" (
    echo Enabling game filter...
    echo ENABLED > "%gameFlagFile%"
    call :PrintYellow "Restart the zapret to apply the changes"
) else (
    echo Disabling game filter...
    del /f /q "%gameFlagFile%"
    call :PrintYellow "Restart the zapret to apply the changes"
)

pause
goto menu


:: Utility functions

:PrintGreen
powershell -Command "Write-Host \"%~1\" -ForegroundColor Green"
exit /b

:PrintRed
powershell -Command "Write-Host \"%~1\" -ForegroundColor Red"
exit /b

:PrintYellow
powershell -Command "Write-Host \"%~1\" -ForegroundColor Yellow"
exit /b