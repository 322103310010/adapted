# AdaptEd Backend API

Flask-based backend for AdaptEd, an adaptive learning platform that generates personalized educational content using AI.

## Features

- Generate learning goals, explanations, summaries, and quiz questions
- Adapt content based on user feedback (simpler, deeper, with analogies)
- Uses OpenRouter API with free LLM models
- RESTful API with CORS support

## Project Structure

```
backend/
├── app.py                          # Main Flask application
├── services/
│   ├── explanation_service.py     # Generates explanations and summaries
│   ├── quiz_service.py             # Creates quiz questions
│   └── adaptation_engine.py        # Adapts content based on feedback
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (with defaults)
└── .env.example                    # Example environment configuration
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

The backend comes pre-configured with OpenRouter's free trial key and a free model. You can use it immediately without any API key setup.

If you want to use your own API key:
1. Get an API key from https://openrouter.ai/keys
2. Update the `.env` file with your key

### 3. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check

```
GET /health
```

Returns server status.

**Response:**
```json
{
  "status": "healthy"
}
```

### Generate Explanation

```
POST /explain
```

Generates a complete learning resource including explanation, summary, and quiz.

**Request Body:**
```json
{
  "subject": "Mathematics",
  "topic": "Quadratic Equations",
  "level": "beginner"
}
```

**Response:**
```json
{
  "session_id": "unique_session_id",
  "learning_goal": "Understand the concept of quadratic equations...",
  "explanation": "A quadratic equation is...",
  "summary": "- Key point 1\n- Key point 2...",
  "quiz": [
    {
      "question": "What is a quadratic equation?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Explanation of the correct answer"
    }
  ]
}
```

### Adapt Content

```
POST /adapt
```

Regenerates the explanation based on user feedback.

**Request Body:**
```json
{
  "session_id": "unique_session_id",
  "feedback": "simpler"
}
```

Supported feedback types:
- `"simpler"` or `"easier"` - Simplifies the explanation
- `"deeper"` or `"more detail"` - Adds more depth
- `"analogy"` or `"example"` - Adds analogies and examples
- Custom feedback text - Adapts based on specific feedback

**Response:**
```json
{
  "explanation": "Adapted explanation based on feedback...",
  "summary": "- Updated key points...",
  "quiz": [
    {
      "question": "Updated quiz question?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Explanation of the correct answer"
    }
  ]
}
```

## Example Usage

### Using curl

```bash
# Generate explanation
curl -X POST http://localhost:5000/explain \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Physics",
    "topic": "Newton'\''s Laws",
    "level": "intermediate"
  }'

# Adapt content
curl -X POST http://localhost:5000/adapt \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your_session_id_here",
    "feedback": "simpler"
  }'
```

### Using Python

```python
import requests

# Generate explanation
response = requests.post('http://localhost:5000/explain', json={
    'subject': 'Computer Science',
    'topic': 'Recursion',
    'level': 'beginner'
})
data = response.json()
session_id = data['session_id']

# Adapt content
response = requests.post('http://localhost:5000/adapt', json={
    'session_id': session_id,
    'feedback': 'add more examples'
})
adapted_data = response.json()
```

## Models

The default configuration uses free models from OpenRouter:
- Default: `meta-llama/llama-3.2-3b-instruct:free`

Other free models you can try:
- `google/gemma-2-9b-it:free`
- `meta-llama/llama-3.1-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`

To change the model, update the `OPENROUTER_MODEL` in your `.env` file.

## Notes

- The backend uses in-memory session storage. Sessions will be lost when the server restarts.
- The free trial API key has rate limits. For production use, get your own key.
- Quiz generation includes fallback questions in case of parsing errors.
