import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-6xl font-bold text-gray-900 mb-6">
            AdaptEd
          </h1>
          <p className="text-2xl text-gray-700 mb-4">
            AI-Powered Adaptive Learning
          </p>
          <p className="text-lg text-gray-600 mb-12 max-w-2xl mx-auto">
            Get personalized explanations that adapt to your understanding level.
            Learn any topic with explanations that evolve as you need them.
          </p>

          <button
            onClick={() => navigate('/topic')}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-8 rounded-lg text-lg transition-colors duration-200 shadow-lg hover:shadow-xl"
          >
            Get Started
          </button>

          <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Personalized Learning
              </h3>
              <p className="text-gray-600">
                Explanations tailored to your current understanding level
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-4xl mb-4">🔄</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Adaptive Content
              </h3>
              <p className="text-gray-600">
                Request simpler explanations, analogies, or deeper insights
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-4xl mb-4">✅</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Interactive Quizzes
              </h3>
              <p className="text-gray-600">
                Test your understanding with generated quiz questions
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
