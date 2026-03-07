@echo off

chcp 65001 >nul

title DeePsHell Launcher
color 0A

:: Автоматическое определение пути к папке со скриптом
set "LAUNCHER_PATH=%~dp0"

:main
cls
set "choice="
echo.
echo    Путь: %LAUNCHER_PATH%
echo    ╔═══════════════════════════════════════════╗
echo    ║            DeePsHell Лаунчер              ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   [1] All Режим                           ║
echo    ║   [2] All2 Режим                          ║
echo    ║   [3] Базовый Режим                       ║
echo    ║   [4] Прочие                              ║
echo    ║                                           ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   [P] Доп. Функции                        ║
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
if "%choice%"=="p" goto pro
if /i "%choice%"=="x" exit

goto main

:all_mode
cls
set "all_choice="
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║                 ALL Режим                 ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   STANDARD:                               ║
echo    ║   [1] General (ALL)                       ║
echo    ║   [2] General (ALL) + nGa                 ║
echo    ║   [3] General (ALL) + nCl                 ║
echo    ║   [4] General (ALL) + nCl + nGa           ║
echo    ║                                           ║
echo    ║   HIDE:                                   ║
echo    ║   [5] Hide (ALL)                          ║
echo    ║   [6] Hide (ALL) + nGa                    ║
echo    ║   [7] Hide (ALL) + nCl                    ║
echo    ║   [8] Hide (ALL) + nCl + nGa              ║
echo    ║                                           ║
echo    ║   [9] Back                                ║
echo    ║                                           ║
echo    ╚═══════════════════════════════════════════╝
echo.
set /p all_choice="   Select: "

if "%all_choice%"=="1" (
    if exist "%LAUNCHER_PATH%General (PsHell) (ALL).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (ALL).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (ALL).bat"
        pause
        goto all_mode
    )
)
if "%all_choice%"=="2" (
    if exist "%LAUNCHER_PATH%General (PsHell) (ALL) (nGa).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (ALL) (nGa).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (ALL) (nGa).bat"
        pause
        goto all_mode
    )
)
if "%all_choice%"=="3" (
    if exist "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL).bat"
        pause
        goto all_mode
    )
)
if "%all_choice%"=="4" (
    if exist "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL) (nGa).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL) (nGa).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL) (nGa).bat"
        pause
        goto all_mode
    )
)
if "%all_choice%"=="5" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL).bat"
        pause
        goto all_mode
    )
)
if "%all_choice%"=="6" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL) (nGa).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL) (nGa).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL) (nGa).bat"
        pause
        goto all_mode
    )
)
if "%all_choice%"=="7" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL).bat"
        pause
        goto all_mode
    )
)
if "%all_choice%"=="8" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL) (nGa).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL) (nGa).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL) (nGa).bat"
        pause
        goto all_mode
    )
)
if "%all_choice%"=="9" goto main

goto all_mode

:all2_mode
cls
set "all2_choice="
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║                ALL2 Режим                 ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   STANDARD:                               ║
echo    ║   [1] General (ALL2)                      ║
echo    ║   [2] General (ALL2) + nGa                ║
echo    ║   [3] General (ALL2) + nCl                ║
echo    ║   [4] General (ALL2) + nCl + nGa          ║
echo    ║                                           ║
echo    ║   HIDE:                                   ║
echo    ║   [5] Hide (ALL2)                         ║
echo    ║   [6] Hide (ALL2) + nGa                   ║
echo    ║   [7] Hide (ALL2) + nCl                   ║
echo    ║   [8] Hide (ALL2) + nCl + nGa             ║
echo    ║                                           ║
echo    ║   [9] Back                                ║
echo    ║                                           ║
echo    ╚═══════════════════════════════════════════╝
echo.
set /p all2_choice="   Select: "

if "%all2_choice%"=="1" (
    if exist "%LAUNCHER_PATH%General (PsHell) (ALL2).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (ALL2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (ALL2).bat"
        pause
        goto all2_mode
    )
)
if "%all2_choice%"=="2" (
    if exist "%LAUNCHER_PATH%General (PsHell) (ALL2) (nGa).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (ALL2) (nGa).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (ALL2) (nGa).bat"
        pause
        goto all2_mode
    )
)
if "%all2_choice%"=="3" (
    if exist "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL2).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL2).bat"
        pause
        goto all2_mode
    )
)
if "%all2_choice%"=="4" (
    if exist "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL2) (nGa).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL2) (nGa).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (nCl) (ALL2) (nGa).bat"
        pause
        goto all2_mode
    )
)
if "%all2_choice%"=="5" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL2).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL2).bat"
        pause
        goto all2_mode
    )
)
if "%all2_choice%"=="6" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL2) (nGa).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL2) (nGa).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (ALL2) (nGa).bat"
        pause
        goto all2_mode
    )
)
if "%all2_choice%"=="7" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL2).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL2).bat"
        pause
        goto all2_mode
    )
)
if "%all2_choice%"=="8" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL2) (nGa).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL2) (nGa).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (ALL2) (nGa).bat"
        pause
        goto all2_mode
    )
)
if "%all2_choice%"=="9" goto main

goto all2_mode

:base_mode
cls
set "base_choice="
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║              Базовый Режим                ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   STANDARD:                               ║
echo    ║   [1] General (Base)                      ║
echo    ║   [2] General (Base) + nCl                ║
echo    ║   [3] General (Base) + nGa                ║
echo    ║   [4] General (Base) + nCl + nGa          ║
echo    ║                                           ║
echo    ║   HIDE:                                   ║
echo    ║   [5] Hide (Base)                         ║
echo    ║   [6] Hide (Base) + nCl                   ║
echo    ║   [7] Hide (Base) + nGa                   ║
echo    ║   [8] Hide (Base) + nCl + nGa             ║
echo    ║                                           ║
echo    ║   [9] Back                                ║
echo    ║                                           ║
echo    ╚═══════════════════════════════════════════╝
echo.
set /p base_choice="   Select: "

if "%base_choice%"=="1" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Base).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Base).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Base).bat"
        pause
        goto base_mode
    )
)
if "%base_choice%"=="2" (
    if exist "%LAUNCHER_PATH%General (PsHell) (nCl) (Base).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (nCl) (Base).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (nCl) (Base).bat"
        pause
        goto base_mode
    )
)
if "%base_choice%"=="3" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Base) (2).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Base) (2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Base) (2).bat"
        pause
        goto base_mode
    )
)
if "%base_choice%"=="4" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Base) (nCl) (2).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Base) (nCl) (2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Base) (nCl) (2).bat"
        pause
        goto base_mode
    )
)
if "%base_choice%"=="5" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (Base).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (Base).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (Base).bat"
        pause
        goto base_mode
    )
)
if "%base_choice%"=="6" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (Base) (nCl) (2).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (Base) (nCl) (2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (Base) (nCl) (2).bat"
        pause
        goto base_mode
    )
)
if "%base_choice%"=="7" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (Base) (2).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (Base) (2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (Base) (2).bat"
        pause
        goto base_mode
    )
)
if "%base_choice%"=="8" (
    if exist "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (Base).bat" (
        call "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (Base).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%General (PsHell) (Hide) (nCl) (Base).bat"
        pause
        goto base_mode
    )
)
if "%base_choice%"=="9" goto main

goto base_mode

:other_mode
cls
set "other_choice="
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║                  Прочие                   ║
echo    ╠═══════════════════════════════════════════╣
echo    ║   Вариант 1                               ║
echo    ║   [1]  Discord                            ║
echo    ║   [2]  Telegram                           ║
echo    ║   [3]  Messenger                          ║
echo    ║   [4]  Youtube                            ║
echo    ║   [5]  MineCraft                          ║
echo    ║   [r]  Roblox                             ║
echo    ║                                           ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   Вариант 2                               ║
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

if "%other_choice%"=="r" (
    if exist "%LAUNCHER_PATH%Roblox (PsHell).bat" (
        call "%LAUNCHER_PATH%Roblox (PsHell).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Roblox (PsHell).bat"
        pause
        goto other_mode
    )
)

if "%other_choice%"=="R" (
    if exist "%LAUNCHER_PATH%Roblox (PsHell).bat" (
        call "%LAUNCHER_PATH%Roblox (PsHell).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Roblox (PsHell).bat"
        pause
        goto other_mode
    )
)

if "%other_choice%"=="1" (
    if exist "%LAUNCHER_PATH%Discord (PsHell).bat" (
        call "%LAUNCHER_PATH%Discord (PsHell).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Discord (PsHell).bat"
        pause
        goto other_mode
    )
)
if "%other_choice%"=="6" (
    if exist "%LAUNCHER_PATH%Discord (PsHell) (2).bat" (
        call "%LAUNCHER_PATH%Discord (PsHell) (2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Discord (PsHell) (2).bat"
        pause
        goto other_mode
    )
)
if "%other_choice%"=="3" (
    if exist "%LAUNCHER_PATH%Messenger (PsHell).bat" (
        call "%LAUNCHER_PATH%Messenger (PsHell).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Messenger (PsHell).bat"
        pause
        goto other_mode
    )
)
if "%other_choice%"=="8" (
    if exist "%LAUNCHER_PATH%Messenger (PsHell) (2).bat" (
        call "%LAUNCHER_PATH%Messenger (PsHell) (2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Messenger (PsHell) (2).bat"
        pause
        goto other_mode
    )
)
if "%other_choice%"=="5" (
    if exist "%LAUNCHER_PATH%MineCraft (PsHell).bat" (
        call "%LAUNCHER_PATH%MineCraft (PsHell).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%MineCraft (PsHell).bat"
        pause
        goto other_mode
    )
)
if "%other_choice%"=="2" (
    if exist "%LAUNCHER_PATH%Telegram (PsHell).bat" (
        call "%LAUNCHER_PATH%Telegram (PsHell).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Telegram (PsHell).bat"
        pause
        goto other_mode
    )
)
if "%other_choice%"=="7" (
    if exist "%LAUNCHER_PATH%Telegram (PsHell) (2).bat" (
        call "%LAUNCHER_PATH%Telegram (PsHell) (2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Telegram (PsHell) (2).bat"
        pause
        goto other_mode
    )
)
if "%other_choice%"=="4" (
    if exist "%LAUNCHER_PATH%Youtube (PsHell).bat" (
        call "%LAUNCHER_PATH%Youtube (PsHell).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Youtube (PsHell).bat"
        pause
        goto other_mode
    )
)
if "%other_choice%"=="9" (
    if exist "%LAUNCHER_PATH%Youtube (PsHell) (2).bat" (
        call "%LAUNCHER_PATH%Youtube (PsHell) (2).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Youtube (PsHell) (2).bat"
        pause
        goto other_mode
    )
)
if "%other_choice%"=="10" goto main

goto other_mode

:pro
cls
set "pro="
echo.
echo    ╔═══════════════════════════════════════════╗
echo    ║              Доп. Функции                 ║
echo    ╠═══════════════════════════════════════════╣
echo    ║                                           ║
echo    ║   [1] Очистка Temp                        ║
echo    ║   [2] Тест Соединения (Токо 1 на 1)       ║
echo    ║   [3] Настройки DNS (Токо 1 на 1)         ║
echo    ║                                           ║
echo    ║   [9] Обратно                             ║
echo    ║                                           ║
echo    ╚═══════════════════════════════════════════╝
echo.
set /p pro="   Select: "

if "%pro%"=="1" (
    if exist "%LAUNCHER_PATH%Очистка Temp.bat" (
        call "%LAUNCHER_PATH%Очистка Temp.bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Очистка Temp.bat"
        pause
        goto pro
    )
)

if "%pro%"=="2" (
    if exist "%LAUNCHER_PATH%Тест Соединения(Токо 1 на 1).bat" (
        call "%LAUNCHER_PATH%Тест Соединения(Токо 1 на 1).bat"
        goto process_complete
    ) else (
        echo Файл не найден: "%LAUNCHER_PATH%Тест Соединения(Токо 1 на 1).bat"
        pause
        goto pro
    )
)

if "%pro%"=="3" (
    goto dns_settings
)

if "%pro%"=="9" goto main

goto pro

:dns_settings
cls
echo.
echo      ╔═══════════════════════════════════════════╗
echo      ║           Настройка DNS серверов          ║
echo      ╚═══════════════════════════════════════════╝

:dns_menu
cls
echo    ╔════════════════════════════════════════════════╗
echo    ║              Выберите действие:                ║
echo    ╠════════════════════════════════════════════════╣
echo    ║ [1] - Установить DNS 8.8.8.8 и 8.8.4.4         ║
echo    ║ [2] - Восстановить автоматическое получение DNS║
echo    ║ [3] - Показать текущие настройки DNS           ║
echo    ║ [4] - Проверить соединение с DNS               ║
echo    ║ [5] - Выход в меню Доп. Функций                ║
echo    ╚════════════════════════════════════════════════╝
echo.
set /p dns_choice="Введите номер [1-5]: "

if "%dns_choice%"=="1" goto SET_DNS
if "%dns_choice%"=="2" goto RESET_DNS
if "%dns_choice%"=="3" goto SHOW_DNS
if "%dns_choice%"=="4" goto TEST_DNS
if "%dns_choice%"=="5" goto pro

echo Неверный выбор! Нажмите любую клавишу...
pause > nul
goto dns_menu

:SET_DNS
echo.
echo Получаем список сетевых подключений...
netsh interface show interface
echo.
set /p adapter="Введите имя сетевого адаптера: "

echo.
echo Устанавливаем DNS серверы...
netsh interface ip set dns name="%adapter%" static 8.8.8.8 primary
netsh interface ip add dns name="%adapter%" 8.8.4.4 index=2

echo.
echo DNS успешно установлены!
echo Основной DNS: 8.8.8.8
echo Альтернативный DNS: 8.8.4.4
echo.
pause
goto dns_menu

:RESET_DNS
echo.
echo Получаем список сетевых подключений...
netsh interface show interface
echo.
set /p adapter="Введите имя сетевого адаптера: "

echo.
echo Восстанавливаем автоматическое получение DNS...
netsh interface ip set dns name="%adapter%" dhcp

echo.
echo Настройки DNS сброшены!
echo.
pause
goto dns_menu

:SHOW_DNS
echo.
echo Текущие настройки DNS:
ipconfig /all | findstr "DNS"
echo.
pause
goto dns_menu

:TEST_DNS
echo.
echo Проверяем соединение с DNS серверами...
echo.
echo Проверка 8.8.8.8:
ping -n 2 8.8.8.8
echo.
echo Проверка 8.8.4.4:
ping -n 2 8.8.4.4
echo.
echo Проверка разрешения имен:
nslookup google.com 8.8.8.8
echo.
pause
goto dns_menu

:process_complete
echo.
echo Процесс завершен. Нажмите любую клавишу для возврата в меню...
pause >nul
goto main