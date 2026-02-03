# DrugDetect AI - Deployment Guide

## 🚀 Quick Deployment to Render (Free)

This guide will help you deploy the DrugDetect AI backend to Render's free tier in under 10 minutes.

---

## Prerequisites

- GitHub account (free)
- Render account (free) - Sign up at https://render.com

---

## Step 1: Push Code to GitHub

### Option A: If you don't have a GitHub repository yet

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Repository name: `drug-detect-ai`
   - Make it **Public** (required for Render free tier)
   - Don't initialize with README (we already have files)
   - Click "Create repository"

2. **Initialize Git and push your code:**

```bash
# Navigate to your project directory
cd C:\Users\sadiq\.gemini\antigravity\scratch\drug-detect-ai

# Initialize Git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - DrugDetect AI platform"

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/drug-detect-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: If you already have a GitHub repository

```bash
cd C:\Users\sadiq\.gemini\antigravity\scratch\drug-detect-ai
git add .
git commit -m "Add deployment configuration"
git push
```

---

## Step 2: Deploy Backend to Render

1. **Sign in to Render:**
   - Go to https://dashboard.render.com
   - Sign up/Login (you can use your GitHub account)

2. **Create a new Web Service:**
   - Click "New +" button in the top right
   - Select "Web Service"

3. **Connect your GitHub repository:**
   - Click "Connect account" if not already connected
   - Find and select your `drug-detect-ai` repository
   - Click "Connect"

4. **Configure the Web Service:**

   Fill in the following settings:

   | Setting | Value |
   |---------|-------|
   | **Name** | `drugdetect-backend` (or any name you prefer) |
   | **Region** | Choose closest to you |
   | **Branch** | `main` |
   | **Root Directory** | `backend` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | **Instance Type** | `Free` |

5. **Advanced Settings (Optional):**
   - Auto-Deploy: `Yes` (recommended - auto-deploys on git push)
   - Health Check Path: `/health`

6. **Click "Create Web Service"**

7. **Wait for deployment:**
   - Render will start building your application
   - This takes 2-5 minutes for the first deployment
   - You'll see logs in real-time
   - Wait for "Your service is live 🎉" message

8. **Copy your backend URL:**
   - It will look like: `https://drugdetect-backend-xxxx.onrender.com`
   - **Save this URL** - you'll need it for the frontend!

---

## Step 3: Test Your Deployed Backend

### Test the Health Endpoint

Open in your browser or use curl:
```bash
curl https://your-backend-url.onrender.com/health
```

Expected response:
```json
{"status":"healthy","timestamp":"2026-02-03T..."}
```

### Test the Stats Endpoint

```bash
curl https://your-backend-url.onrender.com/stats
```

Expected response:
```json
{
  "total_processed": 0,
  "high_risk_alerts": 0,
  "platform_distribution": {
    "Telegram": 0,
    "Instagram": 0
  }
}
```

### View API Documentation

Open in your browser:
```
https://your-backend-url.onrender.com/docs
```

You should see the interactive FastAPI Swagger documentation!

---

## Step 4: Update Frontend to Use Deployed Backend

Now you need to update your `index.html` to connect to the deployed backend instead of localhost.

**Edit `index.html` line 292:**

Change from:
```javascript
const [apiEndpoint] = useState('http://localhost:8000');
```

To:
```javascript
const [apiEndpoint] = useState('https://your-backend-url.onrender.com');
```

**Or use this smart configuration (recommended):**
```javascript
const [apiEndpoint] = useState(
  window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://drugdetect-backend-xxxx.onrender.com'
);
```

This way it works both locally and when deployed!

---

## Step 5: Test Data Simulation with Deployed Backend

Update `simulate_data.py` to use your deployed backend:

**Line 5:**
```python
API_URL = "https://your-backend-url.onrender.com/posts/ingest"
```

Then run:
```bash
python simulate_data.py
```

You should see:
```
Starting simulation...
Ingested: Telegram - Risk: 78% (High)
Ingested: Instagram - Risk: 11% (Low)
...
```

---

## 🎉 Success! Your Backend is Deployed!

Your backend is now live at: `https://your-backend-url.onrender.com`

### What's Next?

1. **Deploy the Frontend:**
   - You can deploy `index.html` to Render Static Site, Vercel, or Netlify
   - Or simply open it locally and it will connect to your deployed backend

2. **Share Your Demo:**
   - Your backend API is publicly accessible
   - Anyone can view the API docs at `/docs`
   - Perfect for presentations and demos!

3. **Monitor Your Service:**
   - View logs in Render dashboard
   - Check metrics and uptime
   - Free tier includes 750 hours/month (enough for always-on)

---

## Important Notes

### Free Tier Limitations

- ⚠️ **Spin down after 15 minutes of inactivity**
  - First request after inactivity takes 30-60 seconds (cold start)
  - Subsequent requests are fast
  
- ✅ **750 hours/month free** (enough for 24/7 uptime)
- ✅ **Automatic HTTPS**
- ✅ **Custom domains** (optional)

### Keeping Your Service Awake

If you want to avoid cold starts, you can:
1. Use a service like UptimeRobot to ping your `/health` endpoint every 5 minutes
2. Upgrade to paid tier ($7/month) for always-on

---

## Troubleshooting

### Build Failed

**Check the logs in Render dashboard for errors:**
- Missing dependencies? Update `requirements.txt`
- Python version issues? Render uses Python 3.11 by default

### Service Won't Start

**Common issues:**
- Wrong start command - should be: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Wrong root directory - should be: `backend`
- Missing `__init__.py` - we already created this!

### CORS Errors

If frontend shows CORS errors:
- Backend already allows all origins with `allow_origins=["*"]`
- This is fine for demos, but in production you should restrict to your frontend domain

---

## Updating Your Deployment

Whenever you make changes:

```bash
git add .
git commit -m "Your commit message"
git push
```

Render will automatically redeploy! (if auto-deploy is enabled)

---

## Cost Breakdown

| Service | Cost |
|---------|------|
| Backend (Render Free) | $0/month |
| Frontend (Local/Render Static) | $0/month |
| **Total** | **$0/month** |

Perfect for demos, hackathons, and presentations! 🎉
