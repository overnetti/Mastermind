import React, { useState } from "react";
import {useLocation} from "react-router-dom";
import './Mastermind.css';

const Mastermind = () => {
  const location = useLocation();
  const { difficulty } = location.state || { difficulty: "Unknown" };
  const [guess, setGuess] = useState("");

  const rules = {
      EASY: ["Rule 1", "Rule 2"],
      NORMAL: ["Rule 3", "Rule 4"],
      HARD: ["Rule 5", "Rule 6"],
      IMPOSSIBLE: ["Rule 7", "Rule 8"],
  }

  const handleGuess = () => {
    // API call
    setGuess("");
  };

  return (
    <div className="game-container">
      <div className="difficulty-banner">
          <h1 className="difficulty-title">Mastermind: {difficulty} Mode </h1>
          <ul className="rules-list">
              {rules[difficulty]?.map((rule, index) => (
                  <li key={index}>{rule}</li>
              )) || <li>No rules available</li>}
          </ul>
      </div>
        <h2 className="combination-header">Guess the Combination!</h2>
        <h4 className="game-text">X correct numbers and Y correct positions</h4>
        <input
            type="text"
            value={guess}
            onChange={(e) => setGuess(e.target.value)}
            placeholder="Enter your guess"
            className="guess-input"
        />
        <button className="guess-button" onClick={handleGuess}>Guess</button>
        <h4 className="game-text">Z guesses remaining</h4>
    </div>
  );
};

export default Mastermind;
