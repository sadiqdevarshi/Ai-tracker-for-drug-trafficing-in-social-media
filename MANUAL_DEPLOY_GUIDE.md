# 📍 Where to Click "Manual Deploy" on Render

## Step-by-Step Visual Guide

### Step 1: Go to Your Service Dashboard

After logging into Render (https://dashboard.render.com), you should see your service `drugdetect-backend` in the list. Click on it.

---

### Step 2: Locate the "Manual Deploy" Button

On your service page, look at the **top right corner** of the page.

You'll see a blue button that says **"Manual Deploy"** with a dropdown arrow (▼).

**Location:** Top right, next to the "Settings" button

---

### Step 3: Click "Manual Deploy"

Click the **"Manual Deploy"** button. A dropdown menu will appear with two options:

1. **"Deploy latest commit"** ← Click this one!
2. **"Clear build cache & deploy"** (use this if you're having persistent issues)

---

### Step 4: Confirm Deployment

After clicking "Deploy latest commit", Render will:
1. Show you a confirmation
2. Start building your application
3. Display real-time logs

---

## 🎯 Quick Reference

**Path:** Dashboard → Your Service → Top Right → "Manual Deploy" → "Deploy latest commit"

**Button Color:** Blue  
**Button Location:** Top right corner of service page  
**Next to:** Settings button  

---

## What Happens After Clicking?

1. **Build Phase** (1-3 minutes)
   - Render installs dependencies
   - You'll see logs like: `pip install -r requirements.txt`

2. **Deploy Phase** (30 seconds)
   - Starts your application
   - You'll see: `Your service is live 🎉`

3. **Success!**
   - Your backend URL becomes active
   - Test with: `curl https://your-app.onrender.com/health`

---

## Still Can't Find It?

### Alternative Method: Settings Page

1. Click **"Settings"** (gear icon, top right)
2. Scroll down to **"Build & Deploy"** section
3. Click **"Manual Deploy"** button there
4. Select **"Deploy latest commit"**

---

## Important: Before Clicking Manual Deploy

Make sure you've updated these settings first:

| Setting | Value |
|---------|-------|
| **Root Directory** | *(leave empty)* |
| **Build Command** | `cd backend && pip install -r requirements.txt` |
| **Start Command** | `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

**How to update:**
1. Click "Settings" (top right)
2. Scroll to "Build & Deploy" section
3. Edit the fields
4. Click "Save Changes"
5. **THEN** click "Manual Deploy"

---

## Troubleshooting

### "I don't see Manual Deploy button"
- Make sure you're on the service page (not the main dashboard)
- Try refreshing the page
- Check if you're logged in

### "Deploy fails immediately"
- Check the logs for error messages
- Verify your settings match the table above
- Try "Clear build cache & deploy" option

---

## Need More Help?

If you're still stuck, take a screenshot of your Render page and I'll help you identify where to click!
