# 📚 StudyAI — Full-Stack AI Study Assistant

A complete web application: React frontend (Vercel) + Flask backend (Render) powered by HuggingFace Transformers.

---

## 🗂 Project Structure

```
studyai/
├── backend/
│   ├── app.py              ← Flask app + API endpoints
│   ├── ai_pipeline.py      ← HuggingFace summarization + Q&A
│   ├── planner.py          ← Weekly study plan generator
│   ├── requirements.txt    ← Python dependencies
│   └── render.yaml         ← Render deployment config
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── vercel.json         ← Vercel deployment config
│   ├── .env.example        ← Copy to .env and fill in
│   └── src/
│       ├── main.jsx
│       ├── index.css       ← Global styles + CSS variables
│       ├── api.js          ← Centralised Axios config
│       ├── App.jsx
│       ├── App.css
│       └── components/
│           ├── Header.jsx
│           ├── ChatPanel.jsx  + ChatPanel.css
│           ├── SummaryPanel.jsx + SummaryPanel.css
│           ├── PlannerPanel.jsx + PlannerPanel.css
│           └── TodoPanel.jsx  + TodoPanel.css
│
└── README.md
```

---

## ⚙️ Running Locally

### Prerequisites
- Python 3.9+
- Node.js 18+
- ~2 GB free disk space (for AI models)
- 4 GB RAM minimum (8 GB recommended)

---

### Step 1 — Backend

```bash
cd backend

# Create & activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Start Flask
python app.py
```

✅ Flask runs at **http://localhost:5000**

> **First run:** HuggingFace downloads ~2 GB of models. This is a one-time operation; models are cached in `~/.cache/huggingface/`.

---

### Step 2 — Frontend

```bash
cd frontend

# Copy env file
cp .env.example .env
# .env already points to http://localhost:5000 — no changes needed for local dev

# Install Node packages
npm install

# Start dev server
npm run dev
```

✅ React runs at **http://localhost:3000**

---

## 🔌 API Reference

| Method | Endpoint     | Request Body                                         | Response                        |
|--------|-------------|------------------------------------------------------|---------------------------------|
| GET    | `/`          | —                                                    | `{ status, message }`           |
| POST   | `/chat`      | `{ message: string, context?: string }`              | `{ reply: string }`             |
| POST   | `/summarize` | `{ text: string }`                                   | `{ summary: string }`           |
| POST   | `/planner`   | `{ subjects: string[], hours_per_day: number }`      | `{ plan: { [day]: session[] } }`|

### Session object
```json
{ "subject": "Math", "duration": "1 hour", "tip": "Practice ≥5 problems." }
```

---

## 🚀 Deployment

### Backend → Render

1. Push your repo to GitHub.
2. Go to **render.com** → **New** → **Web Service** → connect your repo.
3. Set **Root Directory** to `backend`.
4. Configure:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
   - **Environment:** Python 3
5. Add environment variable:
   - `PYTHON_VERSION` = `3.11`
   - `ALLOWED_ORIGINS` = *(leave blank for now; fill in after Vercel deploy)*
6. Click **Deploy**. Copy the public URL, e.g. `https://studyai-backend.onrender.com`.

> ⚠️ Render's free tier spins down after 15 min of inactivity. The first request after spin-down takes ~30 s.

---

### Frontend → Vercel

1. In `frontend/.env.example`, create `frontend/.env.production`:
   ```
   VITE_API_URL=https://studyai-backend.onrender.com
   ```
2. Push to GitHub.
3. Go to **vercel.com** → **New Project** → import your repo.
4. Set **Root Directory** to `frontend`.
5. Add environment variable in Vercel dashboard:
   - `VITE_API_URL` = `https://studyai-backend.onrender.com`
6. Click **Deploy**. Copy your Vercel URL, e.g. `https://studyai.vercel.app`.

---

### Final step — Fix CORS

Go back to Render → your backend service → **Environment** → update:
```
ALLOWED_ORIGINS = https://studyai.vercel.app
```
Then **redeploy** the backend.

---

## 🧠 AI Models

| Feature           | Model                          | Size     |
|-------------------|-------------------------------|----------|
| Summarization     | `facebook/bart-large-cnn`      | ~1.6 GB  |
| Question-Answering| `deepset/roberta-base-squad2`  | ~500 MB  |

---

## 💡 Usage Tips

| Feature | How to use |
|---------|-----------|
| **Chat Q&A** | Paste notes in the Context box → ask your question |
| **Chat Summarize** | Type `summarize` + your text, or use the Summary panel |
| **Study Planner** | Type subjects separated by commas, set hours/day, click Generate |
| **To-Do** | Press Enter or click + to add; click the circle to complete |
| **Focus Mode** | Click 🔔 in the header — everything dims so you can concentrate |
