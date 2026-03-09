# AdaptEd Backend - Project Overview

## Summary

A complete Flask-based REST API backend for AdaptEd, an adaptive learning platform that uses AI to generate personalized educational content. The system can create explanations, summaries, and quizzes, and adapt content based on learner feedback.

## Key Features

### 1. Content Generation (`/explain` endpoint)
- Generates learning goals tailored to subject, topic, and level
- Creates comprehensive explanations
- Produces concise summaries
- Generates 3 multiple-choice quiz questions
- Returns a session ID for subsequent adaptations

### 2. Content Adaptation (`/adapt` endpoint)
- Adapts explanations based on feedback:
  - **Simpler**: Reduces complexity, uses easier vocabulary
  - **Deeper**: Adds technical details and advanced concepts
  - **Analogy**: Adds real-world examples and metaphors
- Regenerates summary and quiz for adapted content
- Maintains session state for continuity

### 3. AI Integration
- Uses OpenRouter API for LLM calls
- Pre-configured with free trial key
- Uses free Llama 3.2 3B model by default
- Supports multiple free models (Gemma, Mistral, etc.)

## Architecture

### Service Layer Pattern

**app.py** (Flask Application)
- Defines REST endpoints
- Handles request validation
- Manages session storage
- Coordinates services

**explanation_service.py**
- Generates learning goals
- Creates explanations
- Produces summaries
- Makes LLM API calls

**quiz_service.py**
- Generates quiz questions
- Parses LLM responses
- Validates question format
- Provides fallback questions

**adaptation_engine.py**
- Analyzes feedback type
- Routes to appropriate adaptation strategy
- Simplifies, deepens, or adds analogies
- Maintains content quality

## Technical Stack

- **Framework**: Flask 3.0.0
- **CORS**: flask-cors 4.0.0
- **HTTP Client**: requests 2.31.0
- **Environment**: python-dotenv 1.0.0
- **AI Provider**: OpenRouter API
- **Default Model**: Llama 3.2 3B Instruct (free)

## API Flow

### Explanation Flow
```
Client Request → /explain endpoint
    ↓
Validate input (subject, topic, level)
    ↓
ExplanationService.generate_learning_goal()
    ↓
ExplanationService.generate_explanation()
    ↓
ExplanationService.generate_summary()
    ↓
QuizService.generate_quiz()
    ↓
Store in session_storage
    ↓
Return complete response with session_id
```

### Adaptation Flow
```
Client Request → /adapt endpoint
    ↓
Validate session_id and feedback
    ↓
Retrieve session data
    ↓
AdaptationEngine.adapt_content()
    ├─→ _simplify_explanation() if "simpler"
    ├─→ _deepen_explanation() if "deeper"
    ├─→ _add_analogy() if "analogy"
    └─→ _general_adaptation() for other feedback
    ↓
ExplanationService.generate_summary()
    ↓
QuizService.generate_quiz()
    ↓
Update session_storage
    ↓
Return adapted response
```

## Configuration

### Environment Variables

**OPENROUTER_API_KEY**
- Default: `sk-or-v1-free-trial-key`
- Free trial key with rate limits
- Replace with your own for production

**OPENROUTER_MODEL**
- Default: `meta-llama/llama-3.2-3b-instruct:free`
- Can use any OpenRouter model
- Free alternatives available

## Session Management

**In-Memory Storage**
- Uses Python dictionary for session data
- Stores: subject, topic, level, explanation, learning_goal
- Session ID format: `{subject}_{topic}_{level}_{hash}`
- Data persists only during server runtime

**Limitations**
- Sessions lost on server restart
- Not suitable for production (use Redis/database)
- No session expiration implemented

## Error Handling

- Input validation on all endpoints
- Try-catch blocks around LLM calls
- Fallback quiz questions on parsing errors
- Descriptive error messages in responses
- Proper HTTP status codes

## Testing

**test_api.py**
- Tests /health endpoint
- Tests /explain with sample data
- Tests /adapt with session ID
- Displays formatted responses
- Requires server running

## Deployment Considerations

### For Production

1. **Replace in-memory storage** with Redis or database
2. **Use your own OpenRouter API key**
3. **Add rate limiting** to prevent abuse
4. **Implement session expiration**
5. **Add authentication** if needed
6. **Use production WSGI server** (gunicorn, uwsgi)
7. **Set up logging** for debugging
8. **Add request timeouts** for LLM calls
9. **Implement retry logic** for API failures
10. **Use environment-specific configs**

### Security Notes

- API keys stored in environment variables
- CORS enabled for all origins (restrict in production)
- No authentication implemented (add if needed)
- Session IDs are predictable (use UUIDs in production)

## Extensibility

### Adding New Adaptation Types

Edit `adaptation_engine.py`:
```python
def adapt_content(self, ...):
    if 'your_feedback_type' in feedback_lower:
        return self._your_custom_method(...)
```

### Adding New Services

1. Create service file in `services/`
2. Add to `services/__init__.py`
3. Import in `app.py`
4. Use in endpoint handlers

### Changing LLM Provider

Modify service files to use different API:
- OpenAI
- Anthropic
- Cohere
- Local models (Ollama)

## Performance

**Response Times** (approximate)
- /health: < 10ms
- /explain: 3-8 seconds (4 LLM calls)
- /adapt: 2-6 seconds (3 LLM calls)

**Optimization Strategies**
- Parallel LLM calls (currently sequential)
- Response caching
- Model selection (faster models)
- Shorter max_tokens
- Batch processing

## Future Enhancements

- [ ] Database integration for sessions
- [ ] User authentication and profiles
- [ ] Learning analytics and tracking
- [ ] Multiple quiz difficulty levels
- [ ] Image generation for visual learners
- [ ] Text-to-speech for explanations
- [ ] Multi-language support
- [ ] Progress tracking across sessions
- [ ] Customizable prompt templates
- [ ] A/B testing for explanations

## License

Open source - free to use and modify.

## Support

For issues or questions:
- Check README.md for detailed documentation
- Review QUICKSTART.md for setup help
- Test with test_api.py
- OpenRouter docs: https://openrouter.ai/docs
