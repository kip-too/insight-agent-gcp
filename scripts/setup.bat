@echo off
echo 🚀 Setting up Insight-Agent on Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not running
    echo Please install Docker Desktop and ensure it's running
    pause
    exit /b 1
)

REM Check if gcloud is installed
gcloud --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Google Cloud CLI is not installed
    echo Please install from https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Check if terraform is installed
terraform --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Terraform is not installed
    echo Please install from https://terraform.io/downloads
    pause
    exit /b 1
)

echo ✅ All prerequisites are installed!

REM Setup Python virtual environment
echo 📦 Setting up Python virtual environment...
cd app
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

echo ✅ Setup complete!
echo.
echo 🎉 To start development:
echo 1. cd app
echo 2. venv\Scripts\activate
echo 3. python main.py
echo.
echo Then visit http://localhost:8080/docs
pause