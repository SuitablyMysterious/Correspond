@echo off
REM =====================================================
REM  Install Script for Correspond on Windows
REM =====================================================

echo =====================================================
echo Setting up the Correspond project on Windows...
echo =====================================================

REM ---- Set Up Python Virtual Environment for Backend ----
cd backend

IF NOT EXIST "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo Python backend setup complete.
cd ..

REM ---- Build the C# Frontend Project ----
echo Building C# UI project...
cd frontend\CorrespondUI

REM This assumes the .NET CLI is available in your PATH.
dotnet build

echo C# UI project build complete.
cd ..\..

echo =====================================================
echo Installation complete.
echo You can now run the Python service and launch the C# UI.
pause
