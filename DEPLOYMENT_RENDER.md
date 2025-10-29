# 🚀 Render.com Deployment Guide

## Prerequisites

1. **GitHub Account** - Code should be in GitHub repo
2. **Render Account** - Sign up at https://render.com
3. **Google Earth Engine** - Project ID: `gleaming-tube-445109-t2`

---

## Step 1: Prepare Repository

### Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit - Land Cover Classification System"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

---

## Step 2: Deploy Backend on Render

### Option A: Using render.yaml (Automatic)

1. Go to https://render.com/dashboard
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will detect `render.yaml` and create services automatically

### Option B: Manual Setup

1. **Create Web Service:**
   - Go to https://render.com/dashboard
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - **Name**: `land-cover-backend`
     - **Environment**: `Python 3`
     - **Region**: `Oregon (US West)`
     - **Branch**: `main`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 600 --workers 2`

2. **Environment Variables:**
   Add these in Render dashboard:
   ```
   PYTHON_VERSION=3.10.0
   GEE_PROJECT_ID=gleaming-tube-445109-t2
   PORT=5000
   FLASK_ENV=production
   SECRET_KEY=your-random-secret-key-here
   ```

3. **Advanced Settings:**
   - Health Check Path: `/api/health`
   - Auto-Deploy: `Yes`

---

## Step 3: Deploy Frontend

### Option 1: Static Site on Render

1. **Create Static Site:**
   - Click "New" → "Static Site"
   - Connect same GitHub repository
   - Configure:
     - **Name**: `land-cover-frontend`
     - **Branch**: `main`
     - **Build Command**: `cd frontend && npm install && npm run build`
     - **Publish Directory**: `frontend/build`

2. **Environment Variables:**
   ```
   REACT_APP_API_URL=https://land-cover-backend.onrender.com
   ```

### Option 2: Netlify/Vercel (Alternative)

If you prefer, deploy frontend separately on:
- **Netlify**: https://netlify.com
- **Vercel**: https://vercel.com

---

## Step 4: Configure Google Earth Engine

### Get GEE Credentials:

1. **Authenticate locally:**
   ```bash
   earthengine authenticate
   ```

2. **Get credentials file:**
   - Windows: `%USERPROFILE%\.config\earthengine\credentials`
   - Linux/Mac: `~/.config/earthengine/credentials`

3. **Add to Render:**
   - Copy entire credentials file content
   - In Render dashboard, add environment variable:
     - Key: `GEE_CREDENTIALS`
     - Value: (paste credentials content)

---

## Step 5: Update Frontend API URL

### In `frontend/src/App.js`:

Replace `http://localhost:5000` with your Render backend URL:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'https://land-cover-backend.onrender.com';

// Use in axios calls
axios.post(`${API_URL}/api/process-complete`, ...)
```

---

## Step 6: Test Deployment

1. **Backend Health Check:**
   ```
   https://land-cover-backend.onrender.com/api/health
   ```
   Should return: `{"status": "ok", "message": "Server is running"}`

2. **Frontend:**
   ```
   https://land-cover-frontend.onrender.com
   ```
   Should load the application

3. **Test Processing:**
   - Select area
   - Choose MODIS (faster for testing)
   - Process and verify results

---

## Important Notes

### Free Tier Limitations:

1. **Backend:**
   - Spins down after 15 min inactivity
   - First request after spin-down takes 30-60 seconds
   - 750 hours/month free

2. **Storage:**
   - Ephemeral (files deleted on restart)
   - Use cloud storage for permanent files:
     - AWS S3
     - Google Cloud Storage
     - Cloudinary

3. **Processing:**
   - 512 MB RAM on free tier
   - May timeout on large areas
   - Recommend MODIS for free tier

### Upgrade Options:

For production use, consider:
- **Starter Plan** ($7/month): 512 MB RAM, no spin-down
- **Standard Plan** ($25/month): 2 GB RAM, better performance

---

## Environment Variables (Complete List)

### Backend:
```
PYTHON_VERSION=3.10.0
GEE_PROJECT_ID=gleaming-tube-445109-t2
PORT=5000
FLASK_ENV=production
SECRET_KEY=your-random-secret-key
GEE_CREDENTIALS=<paste-credentials-here>
```

### Frontend:
```
REACT_APP_API_URL=https://land-cover-backend.onrender.com
```

---

## Troubleshooting

### Backend won't start:
- Check build logs in Render dashboard
- Verify all dependencies in `requirements.txt`
- Check environment variables

### GEE authentication fails:
- Verify `GEE_CREDENTIALS` environment variable
- Check `GEE_PROJECT_ID` is correct
- Ensure credentials file format is correct

### Frontend can't connect to backend:
- Check CORS settings in `app.py`
- Verify `REACT_APP_API_URL` is correct
- Check backend is running

### Processing times out:
- Use MODIS instead of Sentinel-2
- Select smaller areas
- Consider upgrading Render plan

---

## Monitoring

### Render Dashboard:
- View logs: Click service → "Logs"
- Monitor metrics: CPU, Memory, Requests
- Check health: Service status indicator

### Custom Monitoring:
Add to your app:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

---

## Scaling

### For Production:

1. **Upgrade Plan:**
   - More RAM
   - No spin-down
   - Better performance

2. **Add Redis:**
   - For caching
   - Session management
   - Background jobs

3. **Use Background Workers:**
   - Celery for long tasks
   - Separate worker service

4. **Cloud Storage:**
   - S3 for exports
   - CloudFront CDN
   - Persistent storage

---

## Cost Estimate

### Free Tier:
- Backend: Free (with spin-down)
- Frontend: Free
- Total: $0/month

### Production:
- Backend Starter: $7/month
- Frontend: Free
- Redis: $10/month (optional)
- Storage: ~$5/month
- Total: ~$22/month

---

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Backend service deployed
- [ ] Frontend service deployed
- [ ] Environment variables set
- [ ] GEE credentials configured
- [ ] Health check passing
- [ ] Frontend connects to backend
- [ ] Test processing works
- [ ] Custom domain configured (optional)

---

## Support

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

---

## Quick Deploy Commands

```bash
# 1. Commit changes
git add .
git commit -m "Ready for deployment"
git push

# 2. Render will auto-deploy (if connected)

# 3. Check deployment
curl https://land-cover-backend.onrender.com/api/health
```

---

**Your app is ready for Render deployment!** 🚀

All files created:
- ✅ `render.yaml` - Auto-deployment config
- ✅ `Procfile` - Process definition
- ✅ `runtime.txt` - Python version
- ✅ `build.sh` - Build script
- ✅ `start.sh` - Start script
- ✅ `.dockerignore` - Docker ignore
- ✅ Updated `requirements.txt` - All dependencies

**Next:** Push to GitHub and connect to Render!
