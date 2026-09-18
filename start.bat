@echo off
title NEXORA operator deck
cd /d "%~dp0"
where python >nul 2>&1
if errorlevel 1 (
  echo Python was not found. Run python_installer.bat then try again.
  pause
  exit /b 1
)
python nexora.py
if errorlevel 1 pause
