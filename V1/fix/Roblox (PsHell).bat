@echo off
chcp 65001 > nul
:: 65001 - UTF-8

:maintenance
echo Выполнение обслуживания...
del /q /f %temp%\*.* 2>nul
ipconfig /flushdns
netsh int ip reset >nul
echo Обслуживание завершено

cd /d "%~dp0"
call service.bat load_game_filter
echo:

set "BIN=%~dp0bin\"
set "LISTS=%~dp0Lists\"
set "IPSET=%~dp0IpSet\"
cd /d %BIN%

start "DeePsHell: %~n0" /min "%BIN%DeePsHell.exe" --wf-tcp=1-65000,%GameFilter% --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --wf-udp=80,443,500-1400,3478-3481,5222-5243,9000-65535,%GameFilter% --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" ^

--filter-udp=80,443,49152-65535,%GameFilter% --hostlist="%LISTS%List-Roblox-PsHell.txt" --dpi-desync=multisplit --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=80,443,53405,%GameFilter% --hostlist="%LISTS%List-Roblox-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^


--filter-udp=80,443,49152-65535,%GameFilter% --ipset="%IPSET%Ip-Set-Roblox.txt" --dpi-desync=multisplit --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=80,443,53405,%GameFilter% --ipset="%IPSET%Ip-Set-Roblox.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^