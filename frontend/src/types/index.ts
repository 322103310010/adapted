export interface QuizQuestion {
  question: string;
  options: string[];
  correctAnswer: number;
}

export interface ExplanationResponse {
  learning_goal: string;
  explanation: string;
  summary: string;
  quiz: QuizQuestion[];
}

export interface AdaptRequest {
  current_explanation: string;
  adaptation_type: 'simpler' | 'analogy' | 'deeper';
}
