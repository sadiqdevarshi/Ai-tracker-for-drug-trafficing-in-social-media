# 🚀 Quick Deployment Steps

## Your backend is ready to deploy! Follow these steps:

### 1️⃣ Push to GitHub (5 minutes)

```bash
# Create a new repository on GitHub: https://github.com/new
# Name it: drug-detect-ai
# Make it PUBLIC (required for Render free tier)

# Then run these commands:
git remote add origin https://github.com/YOUR_USERNAME/drug-detect-ai.git
git branch -M main
git push -u origin main
```

### 2️⃣ Deploy on Render (5 minutes)

1. Go to https://dashboard.render.com and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - **Name:** `drugdetect-backend`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`
5. Click "Create Web Service"
6. Wait 2-5 minutes for deployment
7. Copy your backend URL (e.g., `https://drugdetect-backend-xxxx.onrender.com`)

### 3️⃣ Test Your Backend

```bash
# Replace with your actual URL
curl https://your-backend-url.onrender.com/health
```

Should return: `{"status":"healthy","timestamp":"..."}`

### 4️⃣ Update Frontend (Optional)

Edit `index.html` line 292 to use your deployed backend URL:
```javascript
const [apiEndpoint] = useState('https://your-backend-url.onrender.com');
```

---

## ✅ What's Already Done

- ✅ Created `Procfile` for Render
- ✅ Updated `requirements.txt` with production dependencies
- ✅ Created `.gitignore` file
- ✅ Initialized Git repository
- ✅ Committed all files
- ✅ Created comprehensive `DEPLOYMENT.md` guide

## 📝 Next Steps

1. Create GitHub repository
2. Push code to GitHub
3. Deploy on Render
4. Test and enjoy! 🎉

---

**Need help?** Check the detailed guide in `DEPLOYMENT.md`
