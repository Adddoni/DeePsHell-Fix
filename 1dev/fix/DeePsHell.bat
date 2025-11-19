@echo off
chcp 65001 >nul
:: 65001 - UTF-8
title DeePsHell Launcher
color 0A

:main
cls
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║            DeePsHell Лаунчер              ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   [1] All Режим                           ║
echo    ║   [2] All2 Режим                          ║
echo    ║   [3] Базовый Режим                       ║
echo    ║   [4] Прочие                              ║
echo    ║                                           ║
echo    ║   [X] Выход                               ║
echo    ║                                           ║
echo    ╚═══════════════════════════════════════════╝
echo.
set /p choice="   Select: "

if "%choice%"=="1" goto all_mode
if "%choice%"=="2" goto all2_mode
if "%choice%"=="3" goto base_mode
if "%choice%"=="4" goto other_mode
if /i "%choice%"=="x" exit

goto main

:all_mode
cls
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║                 ALL Режим                 ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   STANDARD:                               ║
echo    ║   [1] General (ALL)                       ║
echo    ║   [2] General (ALL) + nSt                 ║
echo    ║   [3] General (ALL) + nCl                 ║
echo    ║   [4] General (ALL) + nCl + nSt           ║
echo    ║                                           ║
echo    ║   HIDE:                                   ║
echo    ║   [5] Hide (ALL)                          ║
echo    ║   [6] Hide (ALL) + nSt                    ║
echo    ║   [7] Hide (ALL) + nCl                    ║
echo    ║   [8] Hide (ALL) + nCl + nSt              ║
echo    ║                                           ║
echo    ║   [9] Back                                ║
echo    ║                                           ║
echo    ╚═══════════════════════════════════════════╝
echo.
set /p all_choice="   Select: "

if "%all_choice%"=="1" (
    call "%LAUNCHER_PATH%General (PsHell) (ALL).bat"
    goto process_complete
)
if "%all_choice%"=="2" (
    call "%LAUNCHER_PATH%General (PsHell) (ALL) (nSt).bat"
    goto process_complete
)
if "%all_choice%"=="3" (
    call "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL).bat"
    goto process_complete
)
if "%all_choice%"=="4" (
    call "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL) (nSt).bat"
    goto process_complete
)
if "%all_choice%"=="5" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL).bat"
    goto process_complete
)
if "%all_choice%"=="6" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL) (nSt).bat"
    goto process_complete
)
if "%all_choice%"=="7" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL).bat"
    goto process_complete
)
if "%all_choice%"=="8" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL) (nSt).bat"
    goto process_complete
)
if "%all_choice%"=="9" goto main

goto all_mode

:all2_mode
cls
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║                ALL2 Режим                 ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   STANDARD:                               ║
echo    ║   [1] General (ALL2)                      ║
echo    ║   [2] General (ALL2) + nSt                ║
echo    ║   [3] General (ALL2) + nCl                ║
echo    ║   [4] General (ALL2) + nCl + nSt          ║
echo    ║                                           ║
echo    ║   HIDE:                                   ║
echo    ║   [5] Hide (ALL2)                         ║
echo    ║   [6] Hide (ALL2) + nSt                   ║
echo    ║   [7] Hide (ALL2) + nCl                   ║
echo    ║   [8] Hide (ALL2) + nCl + nSt             ║
echo    ║                                           ║
echo    ║   [9] Back                                ║
echo    ║                                           ║
echo    ╚═══════════════════════════════════════════╝
echo.
set /p all2_choice="   Select: "

if "%all2_choice%"=="1" (
    call "%LAUNCHER_PATH%General (PsHell) (ALL2).bat"
    goto process_complete
)
if "%all2_choice%"=="2" (
    call "%LAUNCHER_PATH%General (PsHell) (ALL2) (nSt).bat"
    goto process_complete
)
if "%all2_choice%"=="3" (
    call "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL2).bat"
    goto process_complete
)
if "%all2_choice%"=="4" (
    call "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL2) (nSt).bat"
    goto process_complete
)
if "%all2_choice%"=="5" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL2).bat"
    goto process_complete
)
if "%all2_choice%"=="6" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL2) (nSt).bat"
    goto process_complete
)
if "%all2_choice%"=="7" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL2).bat"
    goto process_complete
)
if "%all2_choice%"=="8" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL2) (nSt).bat"
    goto process_complete
)
if "%all2_choice%"=="9" goto main

goto all2_mode

:base_mode
cls
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║              Базовый Режим                ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   STANDARD:                               ║
echo    ║   [1] General (Base)                      ║
echo    ║   [2] General (Base) + nCl                ║
echo    ║   [3] General (Base) + nSt                ║
echo    ║   [4] General (Base) + nCl + nSt          ║
echo    ║                                           ║
echo    ║   HIDE:                                   ║
echo    ║   [5] Hide (Base)                         ║
echo    ║   [6] Hide (Base) + nCl                   ║
echo    ║   [7] Hide (Base) + nSt                   ║
echo    ║   [8] Hide (Base) + nCl + nSt             ║
echo    ║                                           ║
echo    ║   [9] Back                                ║
echo    ║                                           ║
echo    ╚═══════════════════════════════════════════╝
echo.
set /p base_choice="   Select: "

if "%base_choice%"=="1" (
    call "%LAUNCHER_PATH%General (PsHell) (Base).bat"
    goto process_complete
)
if "%base_choice%"=="2" (
    call "%LAUNCHER_PATH%General (PsHell) (nCl) (Base).bat"
    goto process_complete
)
if "%base_choice%"=="3" (
    call "%LAUNCHER_PATH%General (PsHell) (Base) (2).bat"
    goto process_complete
)
if "%base_choice%"=="4" (
    call "%LAUNCHER_PATH%General (PsHell) (Base) (nCl) (2).bat"
    goto process_complete
)
if "%base_choice%"=="5" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (Base).bat"
    goto process_complete
)
if "%base_choice%"=="6" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (Base) (nCl) (2).bat"
    goto process_complete
)
if "%base_choice%"=="7" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (Base) (2).bat"
    goto process_complete
)
if "%base_choice%"=="8" (
    call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (Base).bat"
    goto process_complete
)
if "%base_choice%"=="9" goto main

goto base_mode

:other_mode
cls
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║                  Прочиее                  ║
echo    ╠═══════════════════════════════════════════╣
echo    ║   Варивант 1                              ║
echo    ║   [1]  Discord                            ║
echo    ║   [2]  Telegram                           ║
echo    ║   [3]  Messenger                          ║
echo    ║   [4]  Youtube                            ║
echo    ║   [5]  MineCraft                          ║
echo    ╠═══════════════════════════════════════════╣
echo    ║   Варивант 2                              ║
echo    ║   [6]  Discord (2)                        ║
echo    ║   [7]  Telegram (2)                       ║
echo    ║   [8]  Messenger (2)                      ║
echo    ║   [9]  Youtube (2)                        ║
echo    ║                                           ║
echo    ║   [10] Back                               ║
echo    ║                                           ║
echo    ╚═══════════════════════════════════════════╝
echo.
set /p other_choice="   Select: "

if "%other_choice%"=="1" (
    call "%LAUNCHER_PATH%Discord (PsHell).bat"
    goto process_complete
)
if "%other_choice%"=="6" (
    call "%LAUNCHER_PATH%Discord (PsHell) (2).bat"
    goto process_complete
)
if "%other_choice%"=="3" (
    call "%LAUNCHER_PATH%Messenger (PsHell).bat"
    goto process_complete
)
if "%other_choice%"=="8" (
    call "%LAUNCHER_PATH%Messenger (PsHell) (2).bat"
    goto process_complete
)
if "%other_choice%"=="5" (
    call "%LAUNCHER_PATH%MineCraft (PsHell).bat"
    goto process_complete
)
if "%other_choice%"=="2" (
    call "%LAUNCHER_PATH%Telegram (PsHell).bat"
    goto process_complete
)
if "%other_choice%"=="7" (
    call "%LAUNCHER_PATH%Telegram (PsHell) (2).bat"
    goto process_complete
)
if "%other_choice%"=="4" (
    call "%LAUNCHER_PATH%Youtube (PsHell).bat"
    goto process_complete
)
if "%other_choice%"=="9" (
    call "%LAUNCHER_PATH%Youtube (PsHell) (2).bat"
    goto process_complete
)
if "%other_choice%"=="10" goto main

goto other_mode

:process_complete
echo.
echo Процесс завершен. Нажмите любую клавишу для возврата в меню...
pause >nul
goto main