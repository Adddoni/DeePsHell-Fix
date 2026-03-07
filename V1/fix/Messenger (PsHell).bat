@echo off
chcp 65001 > nul
:: 65001 - UTF-8

:maintenance
echo Выполнение обслуживания...
del /q /f %temp%\*.* 2>nul
ipconfig /flushdns
netsh int ip reset >nul

cd /d "%~dp0"
call service.bat load_game_filter
echo:

set "BIN=%~dp0bin\"
set "LISTS=%~dp0Lists\"
set "IPSET=%~dp0IpSet\"
cd /d %BIN%

start "DeePsHell: %~n0" /min "%BIN%DeePsHell.exe" --wf-tcp=1-65000,%GameFilter% --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --wf-udp=80,443,500-1400,3478-3481,5222-5243,9000-65535,%GameFilter% --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" ^
--filter-udp=19294-19344,50000-50100 --filter-l7=discord,stun --dpi-desync=fake --dpi-desync-repeats=6 --new ^
--filter-tcp=443,2053,2083,2087,2096,8443 --hostlist-domains=discord.media --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-tcp=443,2053,2083,2087,2096,8443 --hostlist-domains=cdn.discordapp.com --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-tcp=80,443,%GameFilter% --hostlist="%LISTS%List-Google-Mete-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-udp=3478,%GameFilter% --hostlist="%LISTS%List-Google-Mete-PsHell.txt" --filter-l7=stun --dpi-desync=udplen --dpi-desync-repeats=6 --dpi-desync-udplen-increment=31 --new ^

--filter-tcp=1-65000,%GameFilter% --hostlist="%LISTS%List-Telegram-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-udp=443,500-1400,3478,5222,10000-56110,%GameFilter% --hostlist="%LISTS%List-Telegram-PsHell.txt" --filter-l7=stun --dpi-desync=udplen --dpi-desync-repeats=6 --dpi-desync-udplen-increment=31 --new ^

--filter-tcp=80,443,%GameFilter% --hostlist="%LISTS%List-Snapchat-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-udp=443,%GameFilter% --hostlist="%LISTS%List-Snapchat-PsHell.txt" --filter-l7=stun --dpi-desync=udplen --dpi-desync-repeats=6 --dpi-desync-udplen-increment=31 --new ^

--filter-tcp=80,443,5223,%GameFilter% --hostlist="%LISTS%List-FaceTime-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-udp=443,3478-3497,6384-16387,16393-16402,%GameFilter% --hostlist="%LISTS%List-FaceTime-PsHell.txt" --filter-l7=stun --dpi-desync=udplen --dpi-desync-repeats=6 --dpi-desync-udplen-increment=31 --new ^

--filter-tcp=443,80,%GameFilter% --hostlist="%LISTS%List-Signal-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-udp=443,3478,10000,%GameFilter% --hostlist="%LISTS%List-Signal-PsHell.txt" --filter-l7=stun --dpi-desync=udplen --dpi-desync-repeats=6 --dpi-desync-udplen-increment=31 --new ^

--filter-tcp=80,4244,5222-5228,5242,%GameFilter% --hostlist="%LISTS%List-WhatsApp-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-udp=443,80,3478-3481,4244,5222-5228,5242-5243,45395,%GameFilter% --hostlist="%LISTS%List-WhatsApp-PsHell.txt" --filter-l7=stun --dpi-desync=udplen --dpi-desync-repeats=6 --dpi-desync-udplen-increment=31 --new ^

--filter-udp=443,%GameFilter% --hostlist="%LISTS%List-Discord-PsHell.txt" --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-udp=50000-50100,%GameFilter% --filter-l7=discord,stun --dpi-desync=fake --dpi-desync-repeats=6 --new ^
--filter-tcp=80,443,%GameFilter% --hostlist="%LISTS%List-Discord-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-tcp=80,443,4244,5242,%GameFilter% --hostlist="%LISTS%List-Viber-PsHell.txt" --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
--filter-udp=443,5243,7985,9785,%GameFilter% --hostlist="%LISTS%List-Viber-PsHell.txt"  --filter-l7=stun --dpi-desync=udplen --dpi-desync-repeats=6 --dpi-desync-udplen-increment=31 --new ^


--filter-udp=50000-50100,%GameFilter%  --ipset="%IPSET%Ip-Set-Discord.txt" --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=80,443,%GameFilter% --ipset="%IPSET%Ip-Set-Discord.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-udp=3478,%GameFilter%  --ipset="%IPSET%Ip-Set-Google-mete.txt" --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=80,443,%GameFilter% --ipset="%IPSET%Ip-Set-Google-mete.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-udp=443,500-1400,3478,5222,10000-56110,%GameFilter%  --ipset="%IPSET%Ip-Set-Telegram.txt" --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=1-65000,%GameFilter% --ipset="%IPSET%Ip-Set-Telegram.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-udp=443,5243,7985,9785,%GameFilter%  --ipset="%IPSET%Ip-Set-Viber.txt" --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=80,443,4244,5242,%GameFilter% --ipset="%IPSET%Ip-Set-Viber.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-udp=443,80,3478-3481,4244,5222-5228,5242-5243,45395,%GameFilter%  --ipset="%IPSET%Ip-Set-WahatsApp.txt" --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-tcp=80,4244,5222-5228,5242,%GameFilter% --ipset="%IPSET%Ip-Set-WahatsApp.txt" --dpi-desync=multisplit --dpi-desync-split-seqovl=681 --dpi-desync-split-pos=1 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
