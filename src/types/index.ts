export interface QuizQuestion {
  question: string;
  options: string[];
  correctAnswer: number;
}

export interface ExplanationResponse {
  session_id: string;
  learning_goal: string;
  explanation: string;
  summary: string;
  quiz: QuizQuestion[];
}

export interface AdaptRequest {
  session_id: string;
  feedback: 'simpler' | 'analogy' | 'deeper';
}