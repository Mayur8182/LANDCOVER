@echo off
echo ============================================================
echo Render.com Deployment Setup
echo ============================================================
echo.

echo Step 1: Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo Error: Git not installed!
    echo Please install Git from: https://git-scm.com/
    pause
    exit /b 1
)
echo Git found!

echo.
echo Step 2: Initialize Git repository...
if not exist ".git\" (
    git init
    echo Git repository initialized
) else (
    echo Git repository already exists
)

echo.
echo Step 3: Add all files...
git add .

echo.
echo Step 4: Commit changes...
git commit -m "Deploy to Render - Land Cover Classification System"

echo.
echo ============================================================
echo NEXT STEPS:
echo ============================================================
echo.
echo 1. Create GitHub repository:
echo    - Go to https://github.com/new
echo    - Create new repository
echo    - Copy the repository URL
echo.
echo 2. Push code to GitHub:
echo    git remote add origin YOUR_GITHUB_REPO_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Deploy on Render:
echo    - Go to https://render.com/dashboard
echo    - Click "New" -^> "Blueprint"
echo    - Connect your GitHub repository
echo    - Render will auto-deploy using render.yaml
echo.
echo 4. Set Environment Variables in Render:
echo    GEE_PROJECT_ID=gleaming-tube-445109-t2
echo    SECRET_KEY=your-random-secret-key
echo.
echo 5. Configure GEE Credentials:
echo    - Run: earthengine authenticate
echo    - Copy credentials from:
echo      %%USERPROFILE%%\.config\earthengine\credentials
echo    - Add as GEE_CREDENTIALS environment variable in Render
echo.
echo ============================================================
echo.
pause
