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

start "DeePsHell: %~n0" /min "%BIN%DeePsHell.exe" --wf-tcp=1-65000 --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" ^

--filter-tcp=80 --hostlist="%LISTS%List-Cloudflare-PsHell.txt" --dpi-desync=fake,split2 --dpi-desync-autottl=62 --dpi-desync-fooling=md5sig --new ^

--filter-tcp=80,443,21,20,8080 --hostlist="%LISTS%List-СurseForge-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^

--filter-tcp=80,443,21,20,8080  --hostlist="%LISTS%List-Modrinth-PsHell.txt" --dpi-desync=multisplit --dpi-desync-split-pos=2,sniext+1 --dpi-desync-split-seqovl=679 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin" --new ^
