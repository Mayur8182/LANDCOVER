# 🚀 Render Deployment Instructions

## Step 1: Get Your GEE Credentials

On your local machine, run:

**Windows:**
```cmd
type %USERPROFILE%\.config\earthengine\credentials
```

**Linux/Mac:**
```bash
cat ~/.config/earthengine/credentials
```

Copy the entire JSON output.

---

## Step 2: Add to Render Dashboard

1. Go to: https://dashboard.render.com/
2. Select your service: **land-cover-backend**
3. Click **Environment** tab
4. Add these variables:

### Required Variables:

**GEE_CREDENTIALS**
- Click "Add Environment Variable"
- Key: `GEE_CREDENTIALS`
- Value: Paste the JSON from Step 1
- Click "Save"

**GEE_PROJECT_ID**
- Key: `GEE_PROJECT_ID`
- Value: `gleaming-tube-445109-t2`

**PYTHON_VERSION**
- Key: `PYTHON_VERSION`
- Value: `3.11.7`

**PORT**
- Key: `PORT`
- Value: `5000`

**FLASK_ENV**
- Key: `FLASK_ENV`
- Value: `production`

---

## Step 3: Deploy

Click "Save Changes" - Render will automatically redeploy.

---

## Step 4: Verify

Check logs for:
```
✅ GEE initialized successfully!
📡 Project: gleaming-tube-445109-t2
```

If you see this, your app is ready! 🎉

---

## Troubleshooting

**Error: "GEE credentials not found"**
- Make sure GEE_CREDENTIALS is added in Render dashboard
- Verify the JSON is valid (no extra spaces or line breaks)

**Error: "Project not found"**
- Check GEE_PROJECT_ID: `gleaming-tube-445109-t2`

---

## Security Note

⚠️ Never commit credentials to Git!
- Credentials are in `.env` (ignored by Git)
- Add them manually in Render dashboard
- Keep them secure and private
