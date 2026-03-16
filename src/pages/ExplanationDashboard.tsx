import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useExplanation } from '../context/ExplanationContext';
import QuizSection from '../components/QuizSection';

const ExplanationDashboard: React.FC = () => {

  const navigate = useNavigate();
  const { explanation, setExplanation, isLoading, setIsLoading } = useExplanation();

  const [adaptationError, setAdaptationError] = useState('');

  if (!explanation) {
    navigate('/topic');
    return null;
  }

  const handleAdapt = async (adaptationType: 'simpler' | 'analogy' | 'deeper') => {

    setAdaptationError('');
    setIsLoading(true);

    try {

      const response = await fetch('http://localhost:5000/adapt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          session_id: explanation.session_id,
          feedback: adaptationType
        })
      });

      if (!response.ok) {
        throw new Error('Failed to adapt explanation');
      }

      const data = await response.json();

      setExplanation({
        ...explanation,
        explanation: data.explanation,
        summary: data.summary,
        quiz: data.quiz
      });

    } catch (err) {

      console.error(err);
      setAdaptationError('Failed to adapt explanation. Please try again.');

    } finally {

      setIsLoading(false);

    }
  };

  return (

    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">

      <div className="container mx-auto px-4 py-8">

        <div className="max-w-5xl mx-auto">

          <div className="flex justify-between items-center mb-8">

            <button
              onClick={() => navigate('/topic')}
              className="text-blue-600 hover:text-blue-700 flex items-center gap-2"
            >
              ← New Topic
            </button>

            <h1 className="text-3xl font-bold text-gray-900">AdaptEd</h1>

            <div className="w-24"></div>

          </div>

          {isLoading && (
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 text-blue-700 rounded-lg text-center">
              Loading...
            </div>
          )}

          {adaptationError && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
              {adaptationError}
            </div>
          )}

          <div className="space-y-6">

            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-700 mb-2">Learning Goal</h2>
              <p className="text-lg text-gray-900">{explanation.learning_goal}</p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Explanation</h2>
              <div className="prose prose-lg max-w-none text-gray-700 whitespace-pre-wrap">
                {explanation.explanation}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Summary</h2>
              <p className="text-gray-700 leading-relaxed">{explanation.summary}</p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">

              <h2 className="text-2xl font-bold text-gray-900 mb-4">Adapt Your Learning</h2>

              <p className="text-gray-600 mb-4">
                Need a different approach? Choose how you'd like to adjust this explanation:
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

                <button
                  onClick={() => handleAdapt('simpler')}
                  disabled={isLoading}
                  className="bg-green-600 hover:bg-green-700 disabled:bg-gray-300 text-white font-semibold py-4 px-6 rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
                >
                  <div className="text-2xl mb-2">📉</div>
                  Explain Simpler
                </button>

                <button
                  onClick={() => handleAdapt('analogy')}
                  disabled={isLoading}
                  className="bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-300 text-white font-semibold py-4 px-6 rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
                >
                  <div className="text-2xl mb-2">💡</div>
                  Give Analogy
                </button>

                <button
                  onClick={() => handleAdapt('deeper')}
                  disabled={isLoading}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-semibold py-4 px-6 rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
                >
                  <div className="text-2xl mb-2">📈</div>
                  Go Deeper
                </button>

              </div>

            </div>

            <QuizSection questions={explanation.quiz} />

          </div>

        </div>

      </div>

    </div>

  );

};

export default ExplanationDashboard;