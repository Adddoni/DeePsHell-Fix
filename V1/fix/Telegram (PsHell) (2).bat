@echo off
chcp 65001 > nul
:: 65001 - UTF-8

cd /d "%~dp0"
call service.bat load_game_filter
echo:

set "BIN=%~dp0bin\"
set "LISTS=%~dp0Lists\"
set "IPSET=%~dp0IpSet\"
cd /d %BIN%

start "DeePsHell: %~n0" /min "%BIN%DeePsHell.exe" --wf-tcp=1-65000,%GameFilter% --dpi-desync=fake,split2 --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --wf-udp=80,443,500-1400,3478-3481,5222-5243,9000-65535,%GameFilter% --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" ^

--filter-tcp=1-65000,%GameFilter% --hostlist="%LISTS%List-Telegram-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-udp=443,500-1400,3478,5222,10000-56110,%GameFilter% --hostlist="%LISTS%List-Telegram-PsHell.txt" --filter-l7=stun --dpi-desync=udplen --dpi-desync-repeats=6 --dpi-desync-udplen-increment=31 --new ^

--filter-udp=443,500-1400,3478,5222,10000-56110,%GameFilter%  --ipset="%IPSET%Ip-Set-Telegram.txt" --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=1-65000,%GameFilter% --ipset="%IPSET%Ip-Set-Telegram.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^