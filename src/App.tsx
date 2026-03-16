import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ExplanationProvider } from './context/ExplanationContext';
import LandingPage from './pages/LandingPage';
import TopicInputPage from './pages/TopicInputPage';
import ExplanationDashboard from './pages/ExplanationDashboard';

function App() {
  return (
    <ExplanationProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/topic" element={<TopicInputPage />} />
          <Route path="/dashboard" element={<ExplanationDashboard />} />
        </Routes>
      </Router>
    </ExplanationProvider>
  );
}

export default App;
