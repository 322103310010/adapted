import os
import requests
import json
from typing import List, Dict, Any

class QuizService:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY', 'sk-or-v1-free-trial-key')
        self.base_url = 'https://openrouter.ai/api/v1/chat/completions'
        self.model = os.getenv('OPENROUTER_MODEL', 'meta-llama/llama-3.2-3b-instruct:free')

    def _call_llm(self, prompt: str, system_prompt: str = None) -> str:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:5000',
            'X-Title': 'AdaptEd'
        }

        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})

        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 1500
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            raise Exception(f"LLM API call failed: {str(e)}")

    def generate_quiz(self, subject: str, topic: str, level: str, explanation: str) -> List[Dict[str, Any]]:
        system_prompt = "You are an expert quiz creator. Generate quiz questions in valid JSON format only."

        prompt = f"""Based on the following explanation, create 3 multiple-choice quiz questions to test understanding.

Subject: {subject}
Topic: {topic}
Level: {level}

Explanation:
{explanation}

Generate exactly 3 questions in this JSON format:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": 0,
    "explanation": "Why this is correct"
  }}
]

Respond ONLY with valid JSON array, no additional text."""

        try:
            response = self._call_llm(prompt, system_prompt)

            response_clean = response.strip()
            if response_clean.startswith('```json'):
                response_clean = response_clean[7:]
            if response_clean.startswith('```'):
                response_clean = response_clean[3:]
            if response_clean.endswith('```'):
                response_clean = response_clean[:-3]
            response_clean = response_clean.strip()

            quiz_questions = json.loads(response_clean)

            if not isinstance(quiz_questions, list):
                raise ValueError("Response is not a list")

            validated_questions = []
            for q in quiz_questions[:3]:
                if all(key in q for key in ['question', 'options', 'correct_answer', 'explanation']):
                    validated_questions.append({
                        'question': str(q['question']),
                        'options': [str(opt) for opt in q['options']],
                        'correct_answer': int(q['correct_answer']),
                        'explanation': str(q['explanation'])
                    })

            if not validated_questions:
                return self._get_fallback_questions(subject, topic)

            return validated_questions

        except Exception as e:
            return self._get_fallback_questions(subject, topic)

    def _get_fallback_questions(self, subject: str, topic: str) -> List[Dict[str, Any]]:
        return [
            {
                'question': f'What is the main concept of {topic} in {subject}?',
                'options': [
                    'The primary definition and core principle',
                    'An unrelated concept',
                    'A tangential idea',
                    'None of the above'
                ],
                'correct_answer': 0,
                'explanation': f'This question tests basic understanding of {topic}.'
            },
            {
                'question': f'How does {topic} apply in real-world scenarios?',
                'options': [
                    'Through practical applications',
                    'It does not apply',
                    'Only in theoretical contexts',
                    'Randomly'
                ],
                'correct_answer': 0,
                'explanation': f'{topic} has many practical applications in {subject}.'
            },
            {
                'question': f'What is an important characteristic of {topic}?',
                'options': [
                    'Key defining features',
                    'Irrelevant attributes',
                    'Unrelated properties',
                    'No specific characteristics'
                ],
                'correct_answer': 0,
                'explanation': f'Understanding key characteristics helps master {topic}.'
            }
        ]
