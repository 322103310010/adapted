import os
import requests
from typing import Dict, Any

class AdaptationEngine:
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
            'max_tokens': 1200
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            raise Exception(f"LLM API call failed: {str(e)}")

    def adapt_content(self, subject: str, topic: str, level: str, original_explanation: str, feedback: str) -> str:
        feedback_lower = feedback.lower()

        if 'simpler' in feedback_lower or 'easier' in feedback_lower or 'simple' in feedback_lower:
            return self._simplify_explanation(subject, topic, level, original_explanation)
        elif 'deeper' in feedback_lower or 'detail' in feedback_lower or 'more' in feedback_lower or 'advanced' in feedback_lower:
            return self._deepen_explanation(subject, topic, level, original_explanation)
        elif 'analogy' in feedback_lower or 'example' in feedback_lower or 'metaphor' in feedback_lower:
            return self._add_analogy(subject, topic, level, original_explanation)
        else:
            return self._general_adaptation(subject, topic, level, original_explanation, feedback)

    def _simplify_explanation(self, subject: str, topic: str, level: str, original_explanation: str) -> str:
        system_prompt = f"You are an expert {subject} teacher skilled at simplifying complex concepts for learners."

        prompt = f"""The learner found this explanation too complex. Simplify it while keeping the key concepts.

Original Explanation:
{original_explanation}

Create a simpler version that:
- Uses easier vocabulary
- Breaks down complex ideas into smaller steps
- Removes technical jargon where possible
- Uses everyday language
- Is appropriate for a beginner or {level} learner

Simplified Explanation:"""

        return self._call_llm(prompt, system_prompt)

    def _deepen_explanation(self, subject: str, topic: str, level: str, original_explanation: str) -> str:
        system_prompt = f"You are an expert {subject} teacher who can provide deeper insights and advanced details."

        prompt = f"""The learner wants more depth and detail. Expand on this explanation.

Original Explanation:
{original_explanation}

Create a deeper version that:
- Adds more technical details
- Explores underlying mechanisms
- Includes advanced concepts
- Provides more comprehensive coverage
- Connects to related topics

Enhanced Explanation:"""

        return self._call_llm(prompt, system_prompt)

    def _add_analogy(self, subject: str, topic: str, level: str, original_explanation: str) -> str:
        system_prompt = f"You are an expert {subject} teacher skilled at creating memorable analogies and examples."

        prompt = f"""The learner wants analogies and examples to better understand this topic.

Original Explanation:
{original_explanation}

Create a version that:
- Includes relevant real-world analogies
- Uses relatable examples
- Compares the concept to familiar things
- Makes abstract ideas concrete
- Helps visualize the concept

Explanation with Analogies:"""

        return self._call_llm(prompt, system_prompt)

    def _general_adaptation(self, subject: str, topic: str, level: str, original_explanation: str, feedback: str) -> str:
        system_prompt = f"You are an expert {subject} teacher who adapts explanations based on student feedback."

        prompt = f"""The learner has provided feedback on this explanation.

Original Explanation:
{original_explanation}

Student Feedback:
{feedback}

Adapt the explanation based on this feedback while maintaining accuracy and clarity.

Adapted Explanation:"""

        return self._call_llm(prompt, system_prompt)
