@echo off

chcp 65001 > nul
:: 65001 - UTF-8

:diagnostics
@echo off
chcp 65001 >nul
echo === СИСТЕМНАЯ ДИАГНОСТИКА ===
echo.

echo [СЕТЕВЫЕ ИНТЕРФЕЙСЫ]
ipconfig | findstr /C:"IPv4" /C:"IPv6" /C:"адаптер"
echo.

echo [IP-АДРЕСА]
for /f "tokens=1,2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4" /C:"IPv6-адрес"') do (
    echo %%a: %%b
)
echo.

echo [DNS-СЕРВЕРЫ]
ipconfig /all | findstr /C:"DNS серверы"
echo.

echo [ТЕСТ ПРОПУСКНОЙ СПОСОБНОСТИ IPv4]
ping -n 4 8.8.8.8 | findstr "Average"
echo.

echo [ТЕСТ ПРОПУСКНОЙ СПОСОБНОСТИ IPv6]
ping -6 -n 4 2001:4860:4860::8888 | findstr "Average"
echo.

echo [ПРОВЕРКА МАРШРУТИЗАЦИИ IPv6]
route print -6 | findstr "::/0"
echo.

echo ===========================
pause