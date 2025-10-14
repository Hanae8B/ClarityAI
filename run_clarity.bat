@echo off
REM ====================================================
REM ClarityAI Run Script
REM ====================================================

echo.
echo ===============================
echo  Launching ClarityAI
echo ===============================
echo.

REM Step 1: Activate Python environment (if using venv)
REM Uncomment and edit the following line if using a virtual environment
REM call C:\Path\To\venv\Scripts\activate

REM Step 2: Install dependencies (first-time setup)
echo Installing required Python packages...
pip install --upgrade pip
pip install -r C:\ClarityAI\requirements.txt

REM Step 3: Ensure spaCy model is installed
echo Ensuring spaCy model en_core_web_md is available...
python -m spacy download en_core_web_md

REM Step 4: Launch ClarityAI main script
echo Starting ClarityAI...
cd /d C:\ClarityAI\src
python main.py

pause
