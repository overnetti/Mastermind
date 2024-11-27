import React from "react";
import { useNavigate } from "react-router-dom";
import './DifficultyMode.css';

const Difficulty = () => {
  const navigate = useNavigate();

  const handleDifficultySelection = (mode) => {
    // Set the difficulty mode in the API based on input
    navigate("/mastermind", { state: { difficulty: mode } });
  }

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
            <li>Rule 1</li>
          </ul>
        </button>

        <button
            className="normal-mode-button"
            type="submit"
            onClick={() => handleDifficultySelection("NORMAL")}
        >
          <span className="difficulty-title-button">Normal</span>
          <ul className="difficulty-rules">
            <li>Rule 1</li>
          </ul>
        </button>

        <button
            className="hard-mode-button"
            type="submit"
            onClick={() => handleDifficultySelection("HARD")}
        >
          <span className="difficulty-title-button">Hard</span>
          <ul className="difficulty-rules">
            <li>Rule 1</li>
          </ul>
        </button>

        <button
            className="impossible-mode-button"
            type="submit"
            onClick={() => handleDifficultySelection("IMPOSSIBLE")}
        >
          <span className="difficulty-title-button">Impossible</span>
          <ul className="difficulty-rules">
            <li>Rule 1</li>
          </ul>
        </button>
      </div>
    </div>
);
};

export default Difficulty;
