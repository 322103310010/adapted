"""
Prompt Builder Service
Constructs adaptive LLM prompts based on cognitive analysis recommendations
"""

from typing import Dict, List, Optional

try:
    from .cognitive_analyzer import (
        AdaptationRecommendation,
        DifficultyLevel,
        LearningStyle
    )
except ImportError:
    from cognitive_analyzer import (
        AdaptationRecommendation,
        DifficultyLevel,
        LearningStyle
    )


class PromptBuilder:
    """
    Builds adaptive prompts for LLM based on user cognitive profile
    """

    def __init__(self):
        self.base_system_prompt = """You are an adaptive educational assistant specializing in personalized learning.
Your goal is to explain concepts in a way that matches the user's current understanding and learning style."""

        self.difficulty_templates = {
            DifficultyLevel.VERY_SIMPLE: {
                "instruction": "Explain this concept as if teaching a complete beginner. Use everyday language and avoid jargon.",
                "tone": "friendly and encouraging",
                "vocabulary": "simple, everyday words"
            },
            DifficultyLevel.SIMPLE: {
                "instruction": "Explain this concept in simple terms with minimal technical vocabulary.",
                "tone": "clear and supportive",
                "vocabulary": "accessible language with basic technical terms"
            },
            DifficultyLevel.MODERATE: {
                "instruction": "Provide a balanced explanation with appropriate technical terms.",
                "tone": "professional and clear",
                "vocabulary": "standard technical terminology"
            },
            DifficultyLevel.DETAILED: {
                "instruction": "Provide a detailed explanation with technical depth and nuance.",
                "tone": "professional and thorough",
                "vocabulary": "advanced technical terminology"
            },
            DifficultyLevel.ADVANCED: {
                "instruction": "Provide an advanced, comprehensive explanation with technical rigor.",
                "tone": "expert-level and precise",
                "vocabulary": "specialized terminology and formal language"
            }
        }

        self.learning_style_modifiers = {
            LearningStyle.VISUAL: """
- Use descriptive language that helps create mental images
- Describe diagrams, charts, or visual representations
- Use spatial relationships and visual metaphors
- Structure information in visually hierarchical ways""",

            LearningStyle.ANALOGICAL: """
- Use analogies and metaphors extensively
- Compare concepts to familiar, real-world scenarios
- Draw parallels to everyday experiences
- Use storytelling techniques""",

            LearningStyle.TECHNICAL: """
- Emphasize logical structure and formal definitions
- Include technical specifications and precise terminology
- Show systematic relationships and dependencies
- Provide theoretical foundations""",

            LearningStyle.PRACTICAL: """
- Focus on practical applications and use cases
- Provide concrete examples from real situations
- Emphasize how-to guidance and actionable steps
- Connect theory to practice"""
        }

    def build_adaptive_prompt(
        self,
        topic: str,
        recommendation: AdaptationRecommendation,
        user_question: Optional[str] = None,
        context: Optional[str] = None,
        previous_attempt: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Build a complete adaptive prompt based on cognitive recommendations
        """
        system_prompt = self._build_system_prompt(recommendation)
        user_prompt = self._build_user_prompt(
            topic,
            recommendation,
            user_question,
            context,
            previous_attempt
        )

        return {
            "system": system_prompt,
            "user": user_prompt,
            "temperature": self._get_temperature(recommendation),
            "max_tokens": self._get_max_tokens(recommendation)
        }

    def _build_system_prompt(
        self,
        recommendation: AdaptationRecommendation
    ) -> str:
        """
        Construct the system prompt with adaptive parameters
        """
        difficulty_config = self.difficulty_templates[recommendation.difficulty_level]
        style_modifier = self.learning_style_modifiers[recommendation.learning_style]

        prompt_parts = [
            self.base_system_prompt,
            f"\nCurrent Difficulty Level: {recommendation.difficulty_level.name}",
            f"\n{difficulty_config['instruction']}",
            f"\nTone: {difficulty_config['tone']}",
            f"\nVocabulary: {difficulty_config['vocabulary']}",
            f"\n\nLearning Style Adaptations:",
            style_modifier
        ]

        if recommendation.use_analogies:
            prompt_parts.append("\n- IMPORTANT: Include relevant analogies to aid understanding")

        if recommendation.use_examples:
            prompt_parts.append("\n- Provide concrete examples to illustrate key points")

        if recommendation.use_visuals:
            prompt_parts.append("\n- Describe visual representations (diagrams, charts, etc.)")

        length_instructions = {
            "brief": "\n\nLength: Keep the explanation concise (2-3 paragraphs maximum)",
            "moderate": "\n\nLength: Provide a balanced explanation (3-5 paragraphs)",
            "comprehensive": "\n\nLength: Provide a thorough, comprehensive explanation"
        }
        prompt_parts.append(length_instructions[recommendation.explanation_length])

        if recommendation.technical_depth > 1:
            prompt_parts.append(f"\n\nTechnical Depth: Include technical details at depth level {recommendation.technical_depth}/3")

        return "".join(prompt_parts)

    def _build_user_prompt(
        self,
        topic: str,
        recommendation: AdaptationRecommendation,
        user_question: Optional[str],
        context: Optional[str],
        previous_attempt: Optional[str]
    ) -> str:
        """
        Construct the user prompt with context and adaptations
        """
        prompt_parts = []

        if context:
            prompt_parts.append(f"Context: {context}\n")

        if previous_attempt:
            prompt_parts.append(f"Previous explanation was not clear. Please try a different approach.\n")
            prompt_parts.append(self._get_regeneration_guidance(recommendation))

        if user_question:
            prompt_parts.append(f"Question: {user_question}\n")
        else:
            prompt_parts.append(f"Topic: {topic}\n")

        prompt_parts.append(f"\nPlease explain this concept.")

        return "\n".join(prompt_parts)

    def _get_regeneration_guidance(
        self,
        recommendation: AdaptationRecommendation
    ) -> str:
        """
        Provide specific guidance for regenerated explanations
        """
        if recommendation.learning_style == LearningStyle.ANALOGICAL:
            return "Try using a different analogy or metaphor.\n"
        elif recommendation.learning_style == LearningStyle.VISUAL:
            return "Try describing it from a different visual perspective.\n"
        elif recommendation.learning_style == LearningStyle.PRACTICAL:
            return "Try using a different practical example or use case.\n"
        else:
            return "Try restructuring the explanation with a different approach.\n"

    def _get_temperature(self, recommendation: AdaptationRecommendation) -> float:
        """
        Determine appropriate temperature for LLM based on recommendation
        """
        if recommendation.learning_style == LearningStyle.ANALOGICAL:
            return 0.8
        elif recommendation.learning_style == LearningStyle.TECHNICAL:
            return 0.3
        elif recommendation.difficulty_level in [DifficultyLevel.VERY_SIMPLE, DifficultyLevel.SIMPLE]:
            return 0.7
        else:
            return 0.5

    def _get_max_tokens(self, recommendation: AdaptationRecommendation) -> int:
        """
        Determine appropriate max tokens based on explanation length
        """
        length_tokens = {
            "brief": 300,
            "moderate": 600,
            "comprehensive": 1000
        }
        return length_tokens[recommendation.explanation_length]

    def build_quiz_generation_prompt(
        self,
        topic: str,
        difficulty_level: DifficultyLevel,
        num_questions: int = 5,
        previous_questions: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Build prompt for generating adaptive quiz questions
        """
        difficulty_descriptors = {
            DifficultyLevel.VERY_SIMPLE: "very basic comprehension",
            DifficultyLevel.SIMPLE: "basic understanding",
            DifficultyLevel.MODERATE: "intermediate application",
            DifficultyLevel.DETAILED: "detailed analysis",
            DifficultyLevel.ADVANCED: "advanced synthesis and evaluation"
        }

        system_prompt = f"""You are an educational assessment expert. Generate quiz questions that test {difficulty_descriptors[difficulty_level]} of the topic.

Question Guidelines:
- Each question should have 4 multiple choice options
- Mark the correct answer clearly
- Questions should progressively build understanding
- Avoid trick questions or ambiguous wording"""

        user_prompt = f"""Topic: {topic}
Difficulty: {difficulty_level.name}
Number of questions: {num_questions}"""

        if previous_questions:
            user_prompt += f"\n\nAvoid repeating these previous questions:\n"
            user_prompt += "\n".join(f"- {q}" for q in previous_questions[:5])

        user_prompt += """\n\nGenerate quiz questions in the following JSON format:
{
  "questions": [
    {
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Brief explanation of the correct answer"
    }
  ]
}"""

        return {
            "system": system_prompt,
            "user": user_prompt,
            "temperature": 0.7,
            "max_tokens": 1500
        }

    def apply_feedback_adjustment(
        self,
        original_prompt: Dict[str, str],
        feedback_type: str,
        recommendation: AdaptationRecommendation
    ) -> Dict[str, str]:
        """
        Modify prompt based on user feedback (simpler/deeper/analogy)
        """
        adjusted_prompt = original_prompt.copy()

        if feedback_type == "simpler":
            adjusted_prompt["system"] += "\n\nUSER FEEDBACK: Make this explanation simpler and more accessible."
            adjusted_prompt["temperature"] = 0.7

        elif feedback_type == "deeper":
            adjusted_prompt["system"] += "\n\nUSER FEEDBACK: Provide more depth and technical detail."
            adjusted_prompt["temperature"] = 0.4

        elif feedback_type == "analogy":
            adjusted_prompt["system"] += "\n\nUSER FEEDBACK: Use analogies and metaphors to explain this concept."
            adjusted_prompt["temperature"] = 0.8

        return adjusted_prompt

    def build_followup_prompt(
        self,
        original_topic: str,
        user_followup: str,
        conversation_history: List[Dict[str, str]],
        recommendation: AdaptationRecommendation
    ) -> Dict[str, str]:
        """
        Build prompt for follow-up questions while maintaining context
        """
        system_prompt = self._build_system_prompt(recommendation)
        system_prompt += "\n\nYou are continuing an educational conversation. Maintain consistency with previous explanations."

        conversation_context = "\n\n".join([
            f"{msg['role']}: {msg['content'][:200]}..."
            for msg in conversation_history[-3:]
        ])

        user_prompt = f"""Previous conversation about: {original_topic}

Recent context:
{conversation_context}

Follow-up question: {user_followup}

Please answer the follow-up question while building on the previous explanation."""

        return {
            "system": system_prompt,
            "user": user_prompt,
            "temperature": self._get_temperature(recommendation),
            "max_tokens": self._get_max_tokens(recommendation)
        }


def create_adaptive_prompt_from_data(
    topic: str,
    quiz_history: List[Dict],
    feedback_events: List[Dict],
    regeneration_count: int,
    user_question: Optional[str] = None,
    context: Optional[str] = None
) -> Dict[str, str]:
    """
    Convenience function to create adaptive prompt from raw user data
    """
    try:
        from .cognitive_analyzer import CognitiveAnalyzer, create_cognitive_profile
    except ImportError:
        from cognitive_analyzer import CognitiveAnalyzer, create_cognitive_profile

    performance, feedback_history = create_cognitive_profile(
        quiz_history,
        feedback_events,
        regeneration_count
    )

    analyzer = CognitiveAnalyzer()
    recommendation = analyzer.generate_adaptation_recommendation(
        performance,
        feedback_history
    )

    builder = PromptBuilder()
    previous_attempt = None if regeneration_count == 0 else "Previous attempt failed"

    return builder.build_adaptive_prompt(
        topic=topic,
        recommendation=recommendation,
        user_question=user_question,
        context=context,
        previous_attempt=previous_attempt
    )
