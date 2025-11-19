@echo off
chcp 65001 > nul
:: 65001 - UTF-8

:maintenance
echo Выполнение обслуживания...
del /q /f %temp%\*.* 2>nul
ipconfig /flushdns
netsh int ip reset >nul
echo Обслуживание завершено

pause