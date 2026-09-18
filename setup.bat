@echo off
title NEXORA setup
cd /d "%~dp0"
where python >nul 2>&1
if errorlevel 1 (
  echo Python was not found. Run python_installer.bat first.
  pause
  exit /b 1
)
echo NEXORA uses the Python standard library only — no pip packages required.
python --version
echo.
echo Launch with start.bat
pause
