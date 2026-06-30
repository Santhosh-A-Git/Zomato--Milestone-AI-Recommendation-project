# Deployment Plan: Zomato AI Recommendation System

This document outlines the steps to deploy the application in a decoupled architecture, hosting the **FastAPI Backend on Railway** and the **Vanilla JS Frontend on Vercel**.

## 1. Architecture Overview
- **Backend (Railway)**: A Python FastAPI service that handles data ingestion, filtering, and communication with the Groq LLM API.
- **Frontend (Vercel)**: A static HTML/JS/Tailwind frontend that makes REST API calls to the Railway backend.

---

## 2. Backend Deployment (Railway)

Railway provides native support for Python applications. It will automatically detect your `requirements.txt` and install the dependencies.

### Step-by-Step
1. **Log into Railway**: Go to [Railway.app](https://railway.app/) and sign in with your GitHub account.
2. **Create a New Project**: 
   - Click **New Project** > **Deploy from GitHub repo**.
   - Select your repository: `Santhosh-A-Git/Zomato--Milestone-AI-Recommendation-project`.
3. **Configure the Service**:
   - Railway will automatically start building.
   - Go to the **Variables** tab for your new service and add your Groq API key:
     - `GROQ_API_KEY` = `your-actual-api-key`
   - Go to the **Settings** tab.
   - Under **Deploy**, find the **Custom Start Command** and set it to:
     ```bash
     python -m uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
     ```
4. **Generate a Public URL**:
   - Still in the **Settings** tab, under **Networking**, click **Generate Domain**.
   - Copy this new URL (e.g., `https://zomato-ai-backend-production.up.railway.app`).

---

## 3. Connecting the Frontend to the Backend

Before deploying the frontend, we need to tell it where the backend lives in production. 

1. Open `frontend/src/api.js` in your local code editor.
2. Update the `API_BASE_URL` to dynamically switch between local development and your new Railway production URL. 

Replace line 1 with:
```javascript
// Detect if we are running on localhost, otherwise use the Railway backend URL
const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
const API_BASE_URL = isLocal 
    ? "http://localhost:8000/api" 
    : "https://<YOUR_RAILWAY_URL_HERE>/api"; // <-- Paste your Railway URL here!
```
3. Save the file, commit the changes, and push to GitHub:
```bash
git add frontend/src/api.js
git commit -m "Update API URL for production"
git push
```

---

## 4. Frontend Deployment (Vercel)

Vercel is perfect for deploying static websites instantly.

### Step-by-Step
1. **Log into Vercel**: Go to [Vercel.com](https://vercel.com/) and sign in with GitHub.
2. **Add New Project**:
   - Click **Add New...** > **Project**.
   - Import your repository: `Santhosh-A-Git/Zomato--Milestone-AI-Recommendation-project`.
3. **Configure Project Settings**:
   - **Framework Preset**: Leave as `Other`.
   - **Root Directory**: Click "Edit" and select the `frontend` folder. *(This is critical!)*
   - **Build Command**: Leave blank (we don't need a build step for vanilla JS).
   - **Output Directory**: Leave blank.
4. **Deploy**:
   - Click the **Deploy** button.
   - Vercel will instantly deploy your static files and provide you with a live, production-ready URL!

---

## 5. Post-Deployment Verification
1. Visit your Vercel URL.
2. The Location dropdown should successfully fetch cities from the Railway backend.
3. Submit a request and verify that the Groq LLM returns results correctly.

> **Note on CORS**: The FastAPI backend is currently configured in `src/api/main.py` with `allow_origins=["*"]`. This allows the Vercel frontend to successfully make requests to the Railway backend without Cross-Origin Resource Sharing errors. For stricter security later, you can replace `"*"` with your specific Vercel domain.
