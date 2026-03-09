import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")


class ExplanationService:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = OPENROUTER_MODEL

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found. Check your .env file.")

    def _call_llm(self, prompt: str, system_prompt: str = None) -> str:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "AdaptEd"
        }

        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 800
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()

            return result["choices"][0]["message"]["content"].strip()

        except Exception as e:
            raise Exception(f"LLM API call failed: {str(e)}")

    def generate_learning_goal(self, subject: str, topic: str, level: str) -> str:

        system_prompt = "You are an expert educational content creator. Generate clear and concise learning goals."

        prompt = f"""
Generate a learning goal for the following topic.

Subject: {subject}
Topic: {topic}
Level: {level}

The learning goal should be specific and appropriate for a {level} learner.
Keep it to 1-2 sentences.
"""

        return self._call_llm(prompt, system_prompt)

    def generate_explanation(self, subject: str, topic: str, level: str) -> str:

        system_prompt = f"You are an expert {subject} teacher. Create clear explanations for {level} level students."

        prompt = f"""
Explain the following topic clearly.

Subject: {subject}
Topic: {topic}
Level: {level}

Start simple and gradually build understanding.
Include examples where useful.
"""

        return self._call_llm(prompt, system_prompt)

    def generate_summary(self, explanation: str) -> str:

        system_prompt = "You summarize explanations into short bullet points."

        prompt = f"""
Create a short summary from the explanation below.

Explanation:
{explanation}

Give 3-5 bullet points.
"""

        return self._call_llm(prompt, system_prompt)