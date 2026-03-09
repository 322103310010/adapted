# AdaptEd Backend - Quick Start Guide

Get the AdaptEd backend up and running in 3 simple steps!

## Quick Start

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run the Server

```bash
python app.py
```

Or use the run script:
```bash
./run.sh
```

The server will start at `http://localhost:5000`

### Step 3: Test the API

Open a new terminal and run:

```bash
python test_api.py
```

## What's Included

The backend comes **pre-configured** with:
- OpenRouter free trial API key
- Free Llama 3.2 3B model
- All required dependencies
- Complete API implementation

**No API key setup required!** It works out of the box.

## API Endpoints

### 1. Generate Learning Content

```bash
curl -X POST http://localhost:5000/explain \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Mathematics",
    "topic": "Pythagorean Theorem",
    "level": "beginner"
  }'
```

Returns:
- Learning goal
- Detailed explanation
- Summary
- Quiz questions
- Session ID (save this!)

### 2. Adapt Content

```bash
curl -X POST http://localhost:5000/adapt \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID_HERE",
    "feedback": "simpler"
  }'
```

Feedback options:
- `"simpler"` - Make it easier to understand
- `"deeper"` - Add more detail and depth
- `"analogy"` - Add real-world examples and analogies

Returns:
- Adapted explanation
- Updated summary
- New quiz questions

## File Structure

```
backend/
├── app.py                      # Main Flask application
├── services/
│   ├── explanation_service.py # Generates explanations
│   ├── quiz_service.py         # Creates quiz questions
│   └── adaptation_engine.py    # Adapts content
├── requirements.txt            # Dependencies
├── .env                        # Environment config (pre-configured)
├── test_api.py                 # API test script
├── run.sh                      # Quick start script
└── README.md                   # Full documentation
```

## Troubleshooting

### Port Already in Use

If port 5000 is taken, edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
to use a different port like 5001.

### Module Not Found

Make sure you're in the backend directory and have installed dependencies:
```bash
cd backend
pip install -r requirements.txt
```

## Next Steps

- Check `README.md` for detailed API documentation
- Modify `.env` to use your own OpenRouter API key
- Integrate with a frontend application
- Add more adaptation strategies in `adaptation_engine.py`

## Need Help?

- Full documentation: See `README.md`
- API testing: Run `python test_api.py`
- OpenRouter docs: https://openrouter.ai/docs
