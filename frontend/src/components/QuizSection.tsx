import React, { useState } from 'react';
import type { QuizQuestion } from '../types';

interface QuizSectionProps {
  questions: QuizQuestion[];
}

const QuizSection: React.FC<QuizSectionProps> = ({ questions }) => {
  const [selectedAnswers, setSelectedAnswers] = useState<{ [key: number]: number }>({});
  const [showResults, setShowResults] = useState(false);

  const handleSelectAnswer = (questionIndex: number, optionIndex: number) => {
    if (!showResults) {
      setSelectedAnswers({
        ...selectedAnswers,
        [questionIndex]: optionIndex,
      });
    }
  };

  const handleSubmit = () => {
    setShowResults(true);
  };

  const handleReset = () => {
    setSelectedAnswers({});
    setShowResults(false);
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach((q, index) => {
      if (selectedAnswers[index] === q.correctAnswer) {
        correct++;
      }
    });
    return correct;
  };

  const score = showResults ? calculateScore() : 0;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Quiz</h2>

      {showResults && (
        <div className={`mb-6 p-4 rounded-lg ${score === questions.length ? 'bg-green-50 border border-green-200' : 'bg-blue-50 border border-blue-200'}`}>
          <p className="text-lg font-semibold">
            Score: {score} / {questions.length}
          </p>
        </div>
      )}

      <div className="space-y-6">
        {questions.map((question, qIndex) => (
          <div key={qIndex} className="border-b border-gray-200 pb-6 last:border-b-0">
            <p className="font-semibold text-gray-900 mb-3">
              {qIndex + 1}. {question.question}
            </p>
            <div className="space-y-2">
              {question.options.map((option, oIndex) => {
                const isSelected = selectedAnswers[qIndex] === oIndex;
                const isCorrect = oIndex === question.correctAnswer;
                const showCorrectAnswer = showResults && isCorrect;
                const showIncorrectAnswer = showResults && isSelected && !isCorrect;

                return (
                  <button
                    key={oIndex}
                    onClick={() => handleSelectAnswer(qIndex, oIndex)}
                    disabled={showResults}
                    className={`w-full text-left px-4 py-3 rounded-lg border-2 transition-all ${
                      showCorrectAnswer
                        ? 'bg-green-50 border-green-500'
                        : showIncorrectAnswer
                        ? 'bg-red-50 border-red-500'
                        : isSelected
                        ? 'bg-blue-50 border-blue-500'
                        : 'bg-white border-gray-200 hover:border-blue-300'
                    } ${showResults ? 'cursor-default' : 'cursor-pointer'}`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{String.fromCharCode(65 + oIndex)}.</span>
                      <span>{option}</span>
                      {showCorrectAnswer && <span className="ml-auto text-green-600">✓</span>}
                      {showIncorrectAnswer && <span className="ml-auto text-red-600">✗</span>}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 flex gap-4">
        {!showResults ? (
          <button
            onClick={handleSubmit}
            disabled={Object.keys(selectedAnswers).length !== questions.length}
            className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
          >
            Submit Answers
          </button>
        ) : (
          <button
            onClick={handleReset}
            className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
          >
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};

export default QuizSection;
