@echo off
cd /d "%~dp0"
py -m src.main --vfs vfs_test/vfs_deep.csv
pause