# AdaptEd Frontend

React + TypeScript + Tailwind CSS frontend for the AdaptEd adaptive learning platform.

## Features

- **Landing Page**: Introduction to AdaptEd with feature highlights
- **Topic Input Page**: Enter any topic to learn about
- **Explanation Dashboard**: View personalized explanations with:
  - Learning goals
  - Detailed explanations
  - Summaries
  - Interactive quizzes
  - Adaptation buttons (Explain Simpler, Give Analogy, Go Deeper)

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── QuizSection.tsx       # Interactive quiz component
│   ├── pages/
│   │   ├── LandingPage.tsx       # Home page
│   │   ├── TopicInputPage.tsx    # Topic input form
│   │   └── ExplanationDashboard.tsx  # Main dashboard
│   ├── context/
│   │   └── ExplanationContext.tsx # State management
│   ├── types/
│   │   └── index.ts              # TypeScript types
│   ├── App.tsx                   # Main app component
│   ├── main.tsx                  # Entry point
│   └── index.css                 # Global styles
├── package.json
└── tailwind.config.js
```

## API Integration

The frontend connects to the backend at `http://localhost:8000`:

- `POST /explain` - Get initial explanation for a topic
- `POST /adapt` - Adapt explanation (simpler, analogy, or deeper)

## Development

The development server runs automatically. Access the app at the provided URL.

## Technologies

- React 18
- TypeScript
- Tailwind CSS
- React Router
- Vite
