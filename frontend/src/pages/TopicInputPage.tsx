import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useExplanation } from '../context/ExplanationContext';
import type { ExplanationResponse } from '../types';

const TopicInputPage: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { setExplanation, setIsLoading } = useExplanation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/explain', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
        subject: "General",
        topic: topic,
        level: "beginner"
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get explanation');
      }

      const data: ExplanationResponse = await response.json();
      setExplanation(data);
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to get explanation. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto">
          <button
            onClick={() => navigate('/')}
            className="text-blue-600 hover:text-blue-700 mb-8 flex items-center gap-2"
          >
            ← Back to Home
          </button>

          <div className="bg-white rounded-lg shadow-lg p-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              What do you want to learn?
            </h1>
            <p className="text-gray-600 mb-8">
              Enter any topic and get a personalized explanation with interactive quizzes.
            </p>

            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
                  Topic
                </label>
                <input
                  type="text"
                  id="topic"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g., Quantum Computing, Photosynthesis, Machine Learning..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                />
              </div>

              {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
                  {error}
                </div>
              )}

              <button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
              >
                Get Explanation
              </button>
            </form>
          </div>

          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Pro Tip:</h3>
            <p className="text-gray-700">
              Be specific with your topic for better results. You can always adapt the explanation
              to be simpler or more detailed afterwards.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopicInputPage;
