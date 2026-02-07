# 🏁 Final Presentation Troubleshooting (v1.1)

This guide helps you ensure your **DrugDetect AI** platform is perfect for your live demo.

## ✅ Step 1: Verify the Build
Always check the bottom right of your dashboard. You should see:
- **v1.1-final** (This confirms the latest stable code is running).

## 🛠️ Step 2: Fixing Data Resets (Persistence)
If your dashboard shows **"Storage: In-Memory"** in orange, signals will disappear if the server restarts.

**How to Fix During Demo:**
1.  **Click the orange status pill** ("Storage: In-Memory").
2.  A 2-step guide will pop up.
3.  Add your `MONGODB_URI` to Render's environment variables.
4.  Once the server restarts, you will see **"Storage: Persistent"** in green.

## 🔄 Step 3: Troubleshooting "Old" Dashboard
If you still see the big yellow banner or don't see the v1.1 tag:
- **Action:** Press `Ctrl + F5` (on Windows) or `Cmd + Shift + R` (on Mac).
- This clears your browser's cache and loads the absolute latest version.

## 🚀 Step 4: Using the Simulator
To flood the dashboard with thousands of unique signals:
1.  Open PowerShell in this directory.
2.  Run: `python simulate_data.py`.
3.  The simulator is pre-configured to point to your live URL.

## 🔗 Live URLs
- **Primary:** [https://ai-tracker-for-drug-trafficing-in-social-a16v.onrender.com/](https://ai-tracker-for-drug-trafficing-in-social-a16v.onrender.com/)
- **Backup:** [https://ai-tracker-for-drug-trafficing-in-social-exed.onrender.com/](https://ai-tracker-for-drug-trafficing-in-social-exed.onrender.com/)

---
**Good luck with your presentation!** 🚀
