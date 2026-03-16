from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from services.explanation_service import ExplanationService
from services.adaptation_engine import AdaptationEngine

load_dotenv()

app = Flask(__name__)
CORS(app)

explanation_service = ExplanationService()
adaptation_engine = AdaptationEngine()

# simple in-memory storage
session_storage = {}


# -----------------------------
# EXPLAIN ENDPOINT
# -----------------------------
@app.route('/explain', methods=['POST'])
def explain():
    try:
        data = request.get_json()

        subject = data.get('subject')
        topic = data.get('topic')
        level = data.get('level', 'beginner')

        if not subject or not topic:
            return jsonify({'error': 'Subject and topic are required'}), 400

        # 🔹 Only ONE LLM call (prevents rate limits)
        explanation = explanation_service.generate_explanation(subject, topic, level)

        summary = f"Key idea: {topic} explained simply."

        learning_goal = f"Understand the concept of {topic}."

        quiz_questions = [
            {
                "question": f"What is the main idea behind {topic}?",
                "options": [
                    "Concept explanation",
                    "Random fact",
                    "Unrelated topic",
                    "None"
                ],
                "answer": "Concept explanation"
            }
        ]

        session_id = f"{subject}_{topic}_{level}_{hash(explanation)}"

        session_storage[session_id] = {
            "subject": subject,
            "topic": topic,
            "level": level,
            "explanation": explanation
        }

        return jsonify({
            "session_id": session_id,
            "learning_goal": learning_goal,
            "explanation": explanation,
            "summary": summary,
            "quiz": quiz_questions
        }), 200

    except Exception as e:
        print("ERROR IN /explain:", e)
        return jsonify({"error": str(e)}), 500


# -----------------------------
# ADAPT ENDPOINT
# -----------------------------
@app.route('/adapt', methods=['POST'])
def adapt():
    try:
        data = request.get_json()

        session_id = data.get('session_id')
        feedback = data.get('feedback')

        if not session_id or not feedback:
            return jsonify({'error': 'Session ID and feedback are required'}), 400

        if session_id not in session_storage:
            return jsonify({'error': 'Invalid session ID'}), 404

        session_data = session_storage[session_id]

        # adapt explanation
        adapted_explanation = adaptation_engine.adapt_content(
            subject=session_data["subject"],
            topic=session_data["topic"],
            level=session_data["level"],
            original_explanation=session_data["explanation"],
            feedback=feedback
        )

        # 🔹 Avoid extra LLM calls (keeps system stable)
        summary = f"Adapted explanation for {session_data['topic']}."

        quiz_questions = [
            {
                "question": f"What changed in the explanation of {session_data['topic']}?",
                "options": [
                    "More detailed explanation",
                    "Completely unrelated",
                    "Random text",
                    "Nothing"
                ],
                "answer": "More detailed explanation"
            }
        ]

        session_storage[session_id]["explanation"] = adapted_explanation

        return jsonify({
            "explanation": adapted_explanation,
            "summary": summary,
            "quiz": quiz_questions
        }), 200

    except Exception as e:
        print("ERROR IN /adapt:", e)
        return jsonify({'error': str(e)}), 500


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200


# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    return {"status": "AdaptEd backend running"}


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)