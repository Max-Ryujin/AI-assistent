#!/bin/bash

REM Check if Python is installed
where python3.10 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python 3.10 is not installed. Please install Python 3.10 and try again.
    exit /b 1
)

REM Install CustomTkinter
pip install CustomTkinter

REM Install OpenAI
pip install openai

REM Set up environment variable for OpenAI API key
if "%OSTYPE%"=="linux-gnu" (
  echo Please enter your OpenAI API key:
  set /p API_KEY=
  echo export OPENAI_API_KEY=%API_KEY% >> ~/.bashrc
  source ~/.bashrc
) elif "%OSTYPE%"=="win32" (
  echo Please enter your OpenAI API key:
  set /p API_KEY=
  setx OPENAI_API_KEY %API_KEY%
  setx PATH "%PATH%;C:\Python310\Scripts"
  echo Please restart your terminal or editor for environment variable changes to take effect.
) else (
  echo Unsupported OS
  exit /b 1
)

echo Installation complete!
python Assistant.py
