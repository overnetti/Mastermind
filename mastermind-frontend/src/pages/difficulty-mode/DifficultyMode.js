import React from "react";
import { useNavigate } from "react-router-dom";
import './DifficultyMode.css';

const Difficulty = () => {
  const navigate = useNavigate();

  const handleDifficultySelection = async (mode) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/enter-game', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ difficulty: mode }),
      });

        if (!response.ok) {
          throw new Error(`Failed to set difficulty mode: ${response.statusText}`);
        }

        navigate("/mastermind", { state: { difficulty: mode } });
    } catch (error) {
      console.error('Error setting difficulty:', error.message);
      alert('Failed to set difficulty mode, please try again.');
    }
  };

  return (
    <div className="difficulty-container">
      <h1 className="difficulty-header">Choose Your Difficulty Mode</h1>
      <div className="difficulty-button-container">
        <button
            className="easy-mode-button"
            type="button"
            onClick={() => handleDifficultySelection("EASY")}
        >
          <span className="difficulty-title-button">Easy</span>
          <ul className="difficulty-rules">
            <li>10 guesses</li>
            <li>4 digits</li>
            <li>Digits between 0 and 5</li>
          </ul>
        </button>

        <button
            className="normal-mode-button"
            type="submit"
            onClick={() => handleDifficultySelection("NORMAL")}
        >
          <span className="difficulty-title-button">Normal</span>
          <ul className="difficulty-rules">
            <li>10 guesses</li>
            <li>4 digits</li>
            <li>Digits between 0 and 7</li>
          </ul>
        </button>

        <button
            className="hard-mode-button"
            type="submit"
            onClick={() => handleDifficultySelection("HARD")}
        >
          <span className="difficulty-title-button">Hard</span>
          <ul className="difficulty-rules">
            <li>10 guesses</li>
            <li>6 digits</li>
            <li>Digits between 0 and 9</li>
          </ul>
        </button>

        <button
            className="impossible-mode-button"
            type="submit"
            onClick={() => handleDifficultySelection("IMPOSSIBLE")}
        >
          <span className="difficulty-title-button">Impossible</span>
          <ul className="difficulty-rules">
            <li>5 guesses</li>
            <li>10 digits</li>
            <li>Digits between 0 and 9</li>
          </ul>
        </button>
      </div>
    </div>
);
};

export default Difficulty;
