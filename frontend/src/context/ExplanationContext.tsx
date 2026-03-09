import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { ExplanationResponse } from '../types';

interface ExplanationContextType {
  explanation: ExplanationResponse | null;
  setExplanation: (explanation: ExplanationResponse | null) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

const ExplanationContext = createContext<ExplanationContextType | undefined>(undefined);

export const ExplanationProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [explanation, setExplanation] = useState<ExplanationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <ExplanationContext.Provider
      value={{
        explanation,
        setExplanation,
        isLoading,
        setIsLoading,
      }}
    >
      {children}
    </ExplanationContext.Provider>
  );
};

export const useExplanation = () => {
  const context = useContext(ExplanationContext);
  if (context === undefined) {
    throw new Error('useExplanation must be used within an ExplanationProvider');
  }
  return context;
};
