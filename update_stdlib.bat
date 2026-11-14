@echo off
echo Updating standard library documentation. This may take a while...
python "%~dp0scripts\stdlib_docs.py" --el-root "%~dp0..\el" %*
set "result=%errorlevel%"
if "%result%"=="0" (echo Update complete.) else (echo Update failed. See the error above.)
if "%~1"=="" pause
exit /b %result%
