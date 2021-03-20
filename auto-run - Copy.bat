@echo off
title audio downloader
:loop
echo Ran file
main.py
echo Waiting 10 seconds till next tweet try...
timeout /t 10
goto loop