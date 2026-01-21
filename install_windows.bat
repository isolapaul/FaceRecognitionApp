@echo off
echo ========================================
echo   Face Recognition App - Windows Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.11+ from python.org
    pause
    exit /b 1
)

echo [1/5] Python detected!
python --version

echo.
echo [2/5] Installing dlib-bin (pre-compiled)...
python -m pip install dlib-bin

echo.
echo [3/5] Installing face-recognition (without dependencies)...
python -m pip install --no-deps face-recognition
python -m pip install face-recognition-models

echo.
echo [4/5] Installing other dependencies...
python -m pip install streamlit opencv-python numpy pillow

echo.
echo [5/5] Setup complete!
echo.
echo ========================================
echo   Installation Successful!
echo ========================================
echo.
echo To run the app:
echo   streamlit run app.py
echo.
echo Or if streamlit not in PATH:
echo   python -m streamlit run app.py
echo.
pause
