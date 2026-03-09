"""
Cognitive Analyzer Service
Analyzes user quiz performance, feedback patterns, and engagement
to determine optimal learning adaptations.
"""

from typing import Dict, List, Optional, Literal
from dataclasses import dataclass
from enum import Enum


class DifficultyLevel(Enum):
    VERY_SIMPLE = 1
    SIMPLE = 2
    MODERATE = 3
    DETAILED = 4
    ADVANCED = 5


class LearningStyle(Enum):
    VISUAL = "visual"
    ANALOGICAL = "analogical"
    TECHNICAL = "technical"
    PRACTICAL = "practical"


@dataclass
class UserPerformance:
    correct_answers: int
    total_questions: int
    average_response_time: float
    consecutive_failures: int
    topic_mastery: float


@dataclass
class FeedbackHistory:
    simpler_requests: int
    deeper_requests: int
    analogy_requests: int
    regeneration_count: int
    last_feedback_type: Optional[str]


@dataclass
class AdaptationRecommendation:
    difficulty_level: DifficultyLevel
    learning_style: LearningStyle
    explanation_length: Literal["brief", "moderate", "comprehensive"]
    use_analogies: bool
    use_examples: bool
    use_visuals: bool
    technical_depth: int
    confidence_score: float


class CognitiveAnalyzer:
    """
    Analyzes user cognitive patterns and recommends content adaptations
    """

    def __init__(self):
        self.performance_weights = {
            "quiz_score": 0.4,
            "response_time": 0.2,
            "feedback_pattern": 0.3,
            "regeneration_behavior": 0.1
        }

    def analyze_quiz_performance(
        self,
        performance: UserPerformance
    ) -> Dict[str, float]:
        """
        Analyze quiz performance metrics
        Returns normalized scores for various dimensions
        """
        score_ratio = performance.correct_answers / max(performance.total_questions, 1)

        comprehension_score = score_ratio

        struggle_indicator = min(performance.consecutive_failures / 3.0, 1.0)

        mastery_level = performance.topic_mastery

        speed_factor = self._normalize_response_time(
            performance.average_response_time
        )

        return {
            "comprehension": comprehension_score,
            "struggle": struggle_indicator,
            "mastery": mastery_level,
            "engagement": speed_factor
        }

    def analyze_feedback_pattern(
        self,
        feedback: FeedbackHistory
    ) -> Dict[str, any]:
        """
        Analyze user feedback patterns to identify learning preferences
        """
        total_feedback = (
            feedback.simpler_requests +
            feedback.deeper_requests +
            feedback.analogy_requests
        )

        if total_feedback == 0:
            return {
                "preferred_style": LearningStyle.TECHNICAL,
                "complexity_preference": 0.5,
                "needs_simplification": False,
                "needs_depth": False
            }

        simpler_ratio = feedback.simpler_requests / total_feedback
        deeper_ratio = feedback.deeper_requests / total_feedback
        analogy_ratio = feedback.analogy_requests / total_feedback

        if analogy_ratio > 0.4:
            preferred_style = LearningStyle.ANALOGICAL
        elif simpler_ratio > 0.5:
            preferred_style = LearningStyle.PRACTICAL
        elif deeper_ratio > 0.4:
            preferred_style = LearningStyle.TECHNICAL
        else:
            preferred_style = LearningStyle.VISUAL

        complexity_preference = deeper_ratio - simpler_ratio

        return {
            "preferred_style": preferred_style,
            "complexity_preference": complexity_preference,
            "needs_simplification": simpler_ratio > 0.6,
            "needs_depth": deeper_ratio > 0.5,
            "regeneration_fatigue": feedback.regeneration_count > 3
        }

    def calculate_difficulty_adjustment(
        self,
        quiz_analysis: Dict[str, float],
        feedback_analysis: Dict[str, any],
        current_difficulty: DifficultyLevel
    ) -> DifficultyLevel:
        """
        Determine the appropriate difficulty level based on performance and feedback
        """
        comprehension = quiz_analysis["comprehension"]
        struggle = quiz_analysis["struggle"]
        complexity_pref = feedback_analysis["complexity_preference"]

        adjustment = 0

        if comprehension > 0.8 and struggle < 0.2:
            adjustment += 1
        elif comprehension < 0.5 or struggle > 0.6:
            adjustment -= 1

        if complexity_pref > 0.3:
            adjustment += 1
        elif complexity_pref < -0.3:
            adjustment -= 1

        if feedback_analysis["needs_simplification"]:
            adjustment -= 1

        new_level = max(1, min(5, current_difficulty.value + adjustment))
        return DifficultyLevel(new_level)

    def determine_learning_style(
        self,
        feedback_analysis: Dict[str, any],
        quiz_analysis: Dict[str, float]
    ) -> LearningStyle:
        """
        Determine the most effective learning style for the user
        """
        preferred_style = feedback_analysis["preferred_style"]

        if quiz_analysis["struggle"] > 0.7:
            return LearningStyle.ANALOGICAL

        return preferred_style

    def generate_adaptation_recommendation(
        self,
        performance: UserPerformance,
        feedback: FeedbackHistory,
        current_difficulty: DifficultyLevel = DifficultyLevel.MODERATE
    ) -> AdaptationRecommendation:
        """
        Generate comprehensive adaptation recommendations
        """
        quiz_analysis = self.analyze_quiz_performance(performance)
        feedback_analysis = self.analyze_feedback_pattern(feedback)

        difficulty_level = self.calculate_difficulty_adjustment(
            quiz_analysis,
            feedback_analysis,
            current_difficulty
        )

        learning_style = self.determine_learning_style(
            feedback_analysis,
            quiz_analysis
        )

        if difficulty_level.value <= 2:
            explanation_length = "brief"
        elif difficulty_level.value >= 4:
            explanation_length = "comprehensive"
        else:
            explanation_length = "moderate"

        use_analogies = (
            learning_style == LearningStyle.ANALOGICAL or
            quiz_analysis["struggle"] > 0.5 or
            feedback.analogy_requests > 2
        )

        use_examples = (
            difficulty_level.value <= 3 or
            quiz_analysis["comprehension"] < 0.6
        )

        use_visuals = (
            learning_style == LearningStyle.VISUAL or
            quiz_analysis["engagement"] < 0.5
        )

        technical_depth = min(difficulty_level.value, 3) if learning_style == LearningStyle.TECHNICAL else 1

        confidence_score = self._calculate_confidence(
            quiz_analysis,
            feedback_analysis,
            performance.total_questions
        )

        return AdaptationRecommendation(
            difficulty_level=difficulty_level,
            learning_style=learning_style,
            explanation_length=explanation_length,
            use_analogies=use_analogies,
            use_examples=use_examples,
            use_visuals=use_visuals,
            technical_depth=technical_depth,
            confidence_score=confidence_score
        )

    def _normalize_response_time(self, avg_time: float) -> float:
        """
        Normalize response time to engagement score (0-1)
        Optimal time: 10-30 seconds
        """
        if avg_time < 5:
            return 0.3
        elif 10 <= avg_time <= 30:
            return 1.0
        elif 30 < avg_time <= 60:
            return 0.7
        else:
            return 0.4

    def _calculate_confidence(
        self,
        quiz_analysis: Dict[str, float],
        feedback_analysis: Dict[str, any],
        sample_size: int
    ) -> float:
        """
        Calculate confidence in the adaptation recommendation
        """
        base_confidence = min(sample_size / 10.0, 1.0)

        consistency_bonus = 0.0
        if quiz_analysis["comprehension"] > 0.7 and quiz_analysis["struggle"] < 0.3:
            consistency_bonus = 0.2
        elif quiz_analysis["comprehension"] < 0.3 and quiz_analysis["struggle"] > 0.7:
            consistency_bonus = 0.2

        return min(base_confidence + consistency_bonus, 1.0)


def create_cognitive_profile(
    quiz_history: List[Dict],
    feedback_events: List[Dict],
    regeneration_count: int
) -> tuple[UserPerformance, FeedbackHistory]:
    """
    Helper function to create cognitive profile from raw data
    """
    total_correct = sum(q.get("correct", 0) for q in quiz_history)
    total_questions = len(quiz_history)

    response_times = [q.get("response_time", 20) for q in quiz_history]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 20

    consecutive_failures = 0
    max_consecutive = 0
    for q in reversed(quiz_history):
        if not q.get("correct", False):
            consecutive_failures += 1
            max_consecutive = max(max_consecutive, consecutive_failures)
        else:
            break

    recent_scores = [q.get("correct", 0) for q in quiz_history[-10:]]
    topic_mastery = sum(recent_scores) / len(recent_scores) if recent_scores else 0.5

    performance = UserPerformance(
        correct_answers=total_correct,
        total_questions=total_questions,
        average_response_time=avg_response_time,
        consecutive_failures=max_consecutive,
        topic_mastery=topic_mastery
    )

    simpler_count = sum(1 for f in feedback_events if f.get("type") == "simpler")
    deeper_count = sum(1 for f in feedback_events if f.get("type") == "deeper")
    analogy_count = sum(1 for f in feedback_events if f.get("type") == "analogy")

    last_feedback = feedback_events[-1].get("type") if feedback_events else None

    feedback = FeedbackHistory(
        simpler_requests=simpler_count,
        deeper_requests=deeper_count,
        analogy_requests=analogy_count,
        regeneration_count=regeneration_count,
        last_feedback_type=last_feedback
    )

    return performance, feedback
