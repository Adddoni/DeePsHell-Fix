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

start "DeePsHell: %~n0" /min "%BIN%DeePsHell.exe" --wf-tcp=1-65000,%GameFilter% --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --wf-udp=80,443,500-1400,3478-3481,5222-5243,9000-56110,%GameFilter% --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" ^
--filter-udp=19294-19344,50000-50100 --filter-l7=discord,stun --dpi-desync=fake --dpi-desync-repeats=6 --new ^
--filter-tcp=443,2053,2083,2087,2096,8443 --hostlist-domains=discord.media --dpi-desync=fake,split2 --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-tcp=443,2053,2083,2087,2096,8443 --hostlist-domains=cdn.discordapp.com --dpi-desync=fake,split2 --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-tcp=80,443,8080 --hostlist="%LISTS%List-Cloudflare-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-tcp=1-65000,%GameFilter% --hostlist="%LISTS%List-Messenger-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110,%GameFilter% --hostlist="%LISTS%List-Messenger-PsHell.txt" --filter-l7=stun --dpi-desync=udplen --dpi-desync-repeats=6 --dpi-desync-udplen-increment=31 --new ^

--filter-udp=80,443,3478-3481,19302-19309,%GameFilter% --hostlist="%LISTS%List-See-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-tcp=80,443,1935,%GameFilter% --hostlist="%LISTS%List-See-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=900 --dpi-desync-split-pos=2 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-udp=80,443,500-1400,3478-3497,4244,5222-5228,5242-5243,6384-56110,%GameFilter%  --ipset="%IPSET%Ip-Set-Messenger.txt" --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=1-65000,%GameFilter% --ipset="%IPSET%Ip-Set-Messenger.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-udp=80,443,3478-3481,19302-19309 --ipset="%IPSET%Ip-Set-See.txt" --dpi-desync=multisplit --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=80,443,1935 --ipset="%IPSET%Ip-Set-See.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=900 --dpi-desync-split-pos=2 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^