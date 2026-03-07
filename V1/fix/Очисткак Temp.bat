@echo off

:maintenance
echo Выполнение обслуживания...
del /q /f %temp%\*.* 2>nul
ipconfig /flushdns
netsh int ip reset >nul
echo Обслуживание завершено