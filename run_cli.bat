@echo off
cd /d "%~dp0"
py -m src.main --script scripts/start.txt
pause