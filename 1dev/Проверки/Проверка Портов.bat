@echo off

chcp 65001 > nul
:: 65001 - UTF-8

echo Проверка сетевых соединений DeePsHell...
echo.

echo Основные порты:
netstat -an | findstr ":443" >nul && echo ✓ 443 (HTTPS) - активен || echo ✗ 443 (HTTPS) - неактивен
netstat -an | findstr ":80" >nul && echo ✓ 80 (HTTP) - активен || echo ✗ 80 (HTTP) - неактивen

echo.
echo Активные соединения DeePsHell:
netstat -an | findstr "ESTABLISHED" | findstr "DeePsHell"

echo.
pause