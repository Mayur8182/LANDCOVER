# Troubleshooting Guide

Common issues and their solutions.

## Installation Issues

### 1. Python Virtual Environment

**Problem**: `venv` command not found
```bash
# Windows
python -m venv venv

# If still fails, install:
pip install virtualenv
virtualenv venv
```

**Problem**: Cannot activate virtual environment
```bash
# Windows PowerShell (if execution policy error)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\activate
```

### 2. Package Installation

**Problem**: `pip install` fails
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

**Problem**: GDAL installation fails
```bash
# Windows: Download wheel from
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
pip install GDAL-3.x.x-cpxxx-cpxxx-win_amd64.whl

# Linux
sudo apt-get install gdal-bin libgdal-dev
pip install GDAL==$(gdal-config --version)

# Mac
brew install gdal
pip install GDAL==$(gdal-config --version)
```

**Problem**: TensorFlow installation fails
```bash
# Use specific version
pip install tensorflow==2.15.0

# Or CPU-only version
pip install tensorflow-cpu==2.15.0
```

### 3. Node.js/npm Issues

**Problem**: `npm install` fails
```bash
# Clear cache
npm cache clean --force

# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Node version incompatible
```bash
# Install Node Version Manager (nvm)
# Then install correct version
nvm install 18
nvm use 18
```

## Google Earth Engine Issues

### 1. Authentication

**Problem**: `earthengine authenticate` fails
```bash
# Force re-authentication
earthengine authenticate --force

# If browser doesn't open, use authorization code
earthengine authenticate --authorization-code=YOUR_CODE
```

**Problem**: "Project not found" error
```bash
# Initialize with project
earthengine authenticate --project=your-project-id
```

**Problem**: Authentication works but API fails
```python
# In Python, try:
import ee
ee.Authenticate()
ee.Initialize(project='your-project-id')
```

### 2. API Errors

**Problem**: "User memory limit exceeded"
```python
# Reduce area size or
# Use smaller scale (e.g., scale=30 instead of 10)
```

**Problem**: "Computation timed out"
```python
# Process smaller areas
# Or increase timeout in code
```

## Runtime Issues

### 1. Backend Server

**Problem**: Port 5000 already in use
```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Or change port in .env
PORT=5001
```

**Problem**: "Module not found" error
```bash
# Make sure virtual environment is activated
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

**Problem**: Flask app won't start
```bash
# Check if .env file exists
# Check if all required variables are set
# Run with debug mode
FLASK_DEBUG=1 python app.py
```

### 2. Frontend Server

**Problem**: Port 3000 already in use
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9

# Or set different port
# In package.json, change start script:
"start": "PORT=3001 react-scripts start"
```

**Problem**: "Cannot connect to backend"
```bash
# Check if backend is running on port 5000
# Check proxy setting in frontend/package.json
"proxy": "http://localhost:5000"
```

**Problem**: Map doesn't load
```bash
# Check browser console for errors
# Verify Leaflet CSS is loaded
# Check internet connection (tiles need to download)
```

## Processing Issues

### 1. Imagery Fetching

**Problem**: "No images found"
```
Solutions:
- Expand date range
- Increase cloud cover threshold
- Check if area has Sentinel-2 coverage
- Try different coordinates
```

**Problem**: Download fails
```
Solutions:
- Check internet connection
- Reduce area size
- Try different date range
- Check GEE quota limits
```

### 2. Classification

**Problem**: "Out of memory" during training
```python
Solutions:
- Reduce area size
- Use Random Forest instead of CNN
- Increase system RAM
- Process in smaller batches
```

**Problem**: Low accuracy results
```
Solutions:
- Use larger date range for better composite
- Try different model (CNN vs Random Forest)
- Ensure area has diverse land cover
- Check for cloud contamination
```

**Problem**: Classification takes too long
```
Solutions:
- Use Random Forest (faster than CNN)
- Reduce area size
- Use smaller image scale
- Upgrade hardware
```

### 3. Export Issues

**Problem**: .tif file won't download
```bash
# Check if file exists in exports/
ls exports/

# Check file permissions
chmod 644 exports/*.tif

# Check disk space
df -h
```

**Problem**: .tif file won't open in QGIS
```
Solutions:
- Verify file is not corrupted
- Check file size (should be > 0 bytes)
- Try opening in different GIS software
- Re-export the file
```

## API Issues

### 1. Request Errors

**Problem**: 400 Bad Request
```
Check:
- Request body format (JSON)
- Required parameters present
- Parameter types correct
- Bounds coordinates valid
```

**Problem**: 500 Internal Server Error
```bash
# Check backend logs
tail -f logs/app.log

# Check Flask console output
# Look for Python traceback
```

**Problem**: CORS errors
```python
# In app.py, update CORS settings:
CORS(app, origins=["http://localhost:3000"])
```

### 2. Timeout Issues

**Problem**: Request times out
```
Solutions:
- Increase timeout in frontend
- Process smaller area
- Use faster model (Random Forest)
- Check server resources
```

## Performance Issues

### 1. Slow Processing

**Problem**: Everything is slow
```
Check:
- System resources (CPU, RAM, Disk)
- Internet speed
- Area size (reduce if too large)
- Model type (RF faster than CNN)
```

**Problem**: High memory usage
```
Solutions:
- Close other applications
- Process smaller areas
- Use Random Forest
- Restart application
```

### 2. Disk Space

**Problem**: Running out of disk space
```bash
# Clean old exports
find exports/ -mtime +7 -delete

# Clean old data
find data/ -mtime +7 -delete

# Check disk usage
du -sh data/ exports/
```

## Docker Issues

### 1. Build Errors

**Problem**: Docker build fails
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

**Problem**: Container won't start
```bash
# Check logs
docker-compose logs -f

# Check if ports are available
docker ps -a
```

### 2. Volume Issues

**Problem**: Data not persisting
```bash
# Check volume mounts in docker-compose.yml
# Ensure directories exist on host
mkdir -p data exports models/saved_models logs
```

## Browser Issues

### 1. Display Problems

**Problem**: UI looks broken
```
Solutions:
- Clear browser cache
- Try different browser
- Check browser console for errors
- Disable browser extensions
```

**Problem**: Map not interactive
```
Solutions:
- Check JavaScript is enabled
- Clear browser cache
- Check browser console
- Try incognito mode
```

### 2. Download Issues

**Problem**: File won't download
```
Solutions:
- Check browser download settings
- Try different browser
- Check if popup blocker is active
- Right-click and "Save as"
```

## System-Specific Issues

### Windows

**Problem**: Path too long error
```
Enable long paths:
1. Run gpedit.msc
2. Navigate to: Computer Configuration > Administrative Templates > System > Filesystem
3. Enable "Enable Win32 long paths"
```

**Problem**: Permission denied
```bash
# Run as administrator
# Or change folder permissions
```

### Linux

**Problem**: Permission denied
```bash
# Fix permissions
sudo chown -R $USER:$USER /path/to/project

# Or run with sudo (not recommended)
```

**Problem**: Library not found
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-dev libgdal-dev
```

### Mac

**Problem**: SSL certificate error
```bash
# Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

**Problem**: Command not found
```bash
# Add to PATH in ~/.zshrc or ~/.bash_profile
export PATH="/usr/local/bin:$PATH"
```

## Debugging Tips

### 1. Enable Debug Mode

```python
# In app.py
app.run(debug=True)
```

### 2. Check Logs

```bash
# Backend logs
tail -f logs/app.log

# Frontend logs
# Check browser console (F12)
```

### 3. Test API Directly

```bash
# Use test_api.py
python test_api.py

# Or use curl
curl http://localhost:5000/api/health
```

### 4. Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Node version
node --version
npm --version

# Check Earth Engine
earthengine --version
```

## Getting More Help

### 1. Check Documentation
- README.md
- SETUP_GUIDE.md
- API_DOCUMENTATION.md

### 2. Review Error Messages
- Read full error message
- Check stack trace
- Search error online

### 3. Test Components
- Test backend separately
- Test frontend separately
- Test API endpoints individually

### 4. Simplify Problem
- Use smaller area
- Use default dates
- Use Random Forest model
- Test with known working location

## Common Error Messages

### "ModuleNotFoundError: No module named 'ee'"
```bash
pip install earthengine-api
```

### "ImportError: cannot import name 'PILLOW_VERSION'"
```bash
pip install --upgrade pillow
```

### "RuntimeError: Unable to find gdal"
```bash
# See GDAL installation section above
```

### "Error: ENOSPC: System limit for number of file watchers reached"
```bash
# Linux only
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### "fetch failed" in frontend
```
Check:
- Backend is running
- Correct proxy in package.json
- No CORS issues
- Network connection
```

## Prevention Tips

1. **Always activate virtual environment** before running
2. **Keep dependencies updated** regularly
3. **Test with small areas** first
4. **Monitor disk space** regularly
5. **Check logs** for warnings
6. **Backup trained models** periodically
7. **Use version control** for code changes
8. **Document custom changes**

## Still Having Issues?

1. Check all documentation files
2. Review error messages carefully
3. Test each component separately
4. Try with minimal example
5. Check system requirements
6. Verify all prerequisites installed
7. Look for similar issues online
8. Create minimal reproducible example

---

**Remember**: Most issues are due to:
- Missing dependencies
- Incorrect environment setup
- GEE authentication problems
- Insufficient system resources
- Network connectivity issues

Start with the basics and work your way up!
