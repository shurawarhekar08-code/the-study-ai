# ==============================================================
#  app.py  —  AI Study Assistant · Flask Backend
# ==============================================================
#  Endpoints:
#    POST /chat       → chatbot  (summarize OR question-answer)
#    POST /summarize  → summarize any pasted text
#    POST /planner    → generate a weekly study plan
#
#  Run locally:
#    python app.py
#
#  Deploy on Render:
#    Build command : pip install -r requirements.txt
#    Start command : gunicorn app:app
# ==============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_pipeline import get_summary, get_answer
from planner import generate_study_plan
import os

app = Flask(__name__)

# ── CORS ────────────────────────────────────────────────────
# Allow the React frontend (Vercel or localhost) to call this API.
# In production, replace "*" with your actual Vercel URL, e.g.:
#   CORS(app, origins=["https://your-app.vercel.app"])
CORS(app, origins=os.getenv("ALLOWED_ORIGINS", "*"))


# ── Health check (useful for Render) ────────────────────────
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "StudyAI backend is running 🚀"})


# ── POST /chat ───────────────────────────────────────────────
# Body  : { "message": "...", "context": "..." }
# Returns: { "reply": "..." }
@app.route("/chat", methods=["POST"])
def chat():
    data    = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    context = data.get("context", "").strip()

    if not message:
        return jsonify({"error": "No message provided."}), 400

    # Route to summarization if user says "summarize"
    if "summarize" in message.lower() or "summary" in message.lower():
        text = context if context else message
        reply = get_summary(text)
    else:
        # Question-answering needs context to extract an answer from
        if context:
            reply = get_answer(question=message, context=context)
        else:
            reply = (
                "I need some study material to work with! "
                "Please paste your notes or textbook text in the Context box, "
                "then ask your question."
            )

    return jsonify({"reply": reply})


# ── POST /summarize ──────────────────────────────────────────
# Body  : { "text": "..." }
# Returns: { "summary": "..." }
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided."}), 400
    if len(text.split()) < 30:
        return jsonify({"error": "Text too short — please provide at least 30 words."}), 400

    return jsonify({"summary": get_summary(text)})


# ── POST /planner ─────────────────────────────────────────────
# Body  : { "subjects": ["Math", "Science"], "hours_per_day": 3 }
# Returns: { "plan": { "Monday": [...], ... } }
@app.route("/planner", methods=["POST"])
def planner():
    data         = request.get_json(silent=True) or {}
    subjects     = data.get("subjects", [])
    hours_per_day = int(data.get("hours_per_day", 2))

    if not subjects:
        return jsonify({"error": "Please provide at least one subject."}), 400

    return jsonify({"plan": generate_study_plan(subjects, hours_per_day)})


# ── Start ─────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀  StudyAI backend → http://localhost:{port}")
    app.run(debug=True, port=port)
