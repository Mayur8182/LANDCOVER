# 🔑 Render Environment Variables Setup

## Critical: GEE Credentials Required

Your project **REQUIRES** Google Earth Engine credentials to function. Without them, the app will not work.

---

## Step 1: Get Your GEE Credentials

### On Windows:
```cmd
type %USERPROFILE%\.config\earthengine\credentials
```

### On Linux/Mac:
```bash
cat ~/.config/earthengine/credentials
```

You'll see something like:
```json
{
  "client_id": "xxx.apps.googleusercontent.com",
  "client_secret": "xxx",
  "refresh_token": "xxx",
  "scopes": ["https://www.googleapis.com/auth/earthengine"],
  "type": "authorized_user"
}
```

**Copy this entire JSON content!**

---

## Step 2: Add to Render Dashboard

Go to your Render service → **Environment** tab

### Add These Variables:

#### 1. GEE_CREDENTIALS (REQUIRED)
```
Key: GEE_CREDENTIALS
Value: <paste the entire JSON from credentials file>
```

#### 2. GEE_PROJECT_ID (REQUIRED)
```
Key: GEE_PROJECT_ID
Value: gleaming-tube-445109-t2
```

#### 3. PYTHON_VERSION
```
Key: PYTHON_VERSION
Value: 3.11.7
```

#### 4. PORT
```
Key: PORT
Value: 5000
```

#### 5. FLASK_ENV
```
Key: FLASK_ENV
Value: production
```

---

## Step 3: Update build.sh to Use Credentials

The `build.sh` script will automatically:
1. Create the credentials directory
2. Write the credentials file
3. Authenticate with GEE

---

## Step 4: Verify Deployment

After adding credentials, Render will auto-redeploy.

Check logs for:
```
✓ GEE initialized with project: gleaming-tube-445109-t2
```

If you see this, GEE is working! 🎉

---

## Troubleshooting

### Error: "Please authorize access to your Earth Engine account"
- **Solution**: Add `GEE_CREDENTIALS` environment variable in Render

### Error: "Project not found"
- **Solution**: Verify `GEE_PROJECT_ID` is correct: `gleaming-tube-445109-t2`

### Error: "Invalid credentials"
- **Solution**: Re-run `earthengine authenticate` locally and get fresh credentials

---

## Alternative: Service Account (Production)

For production, use a service account instead:

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Create service account
3. Download JSON key
4. Add to Render as `GEE_SERVICE_ACCOUNT_KEY`

Then update `backend/gee_handler.py`:
```python
import json
service_account = os.getenv('GEE_SERVICE_ACCOUNT_KEY')
if service_account:
    credentials = ee.ServiceAccountCredentials(
        email='your-sa@project.iam.gserviceaccount.com',
        key_data=service_account
    )
    ee.Initialize(credentials)
```

---

## Quick Checklist

- [ ] Get credentials from local machine
- [ ] Add `GEE_CREDENTIALS` to Render
- [ ] Add `GEE_PROJECT_ID` to Render
- [ ] Wait for auto-redeploy
- [ ] Check logs for "✓ GEE initialized"
- [ ] Test API endpoint: `/api/health`

---

**Your app WILL NOT work without GEE credentials!** This is the most important step. 🔑
