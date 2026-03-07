@echo off
chcp 65001 >nul
echo ===== ПРОВЕРКА DEEPSHELL.EXE =====
echo.

cd /d "%~dp0bin"

echo 1. Проверка файла DeePsHell.exe:
if exist "DeePsHell.exe" (
    echo [OK] Файл существует
    echo Размер: %~z0 bytes
) else (
    echo [ERROR] Файл не найден!
    goto :end
)

echo.
echo 2. Попытка запуска без параметров:
echo Запускаем DeePsHell.exe...
DeePsHell.exe
echo Код завершения: %errorlevel%

:end
echo.
pause