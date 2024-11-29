import React, { useState } from "react";
import {useLocation} from "react-router-dom";
import './Mastermind.css';

const Mastermind = () => {
  const location = useLocation();
  const { difficulty } = location.state || { difficulty: "Unknown" };
  const [guess, setGuess] = useState("");
  const [correctNumbers, setCorrectNumbers] = useState(0);
  const [correctPositions, setCorrectPositions] = useState(0);
  const [remainingGuesses, setRemainingGuesses] = useState(null);

  const rules = {
      EASY: ["10 guesses", "4 digits", "Digits between 0 and 5"],
      NORMAL: ["10 guesses", "4 digits", "Digits between 0 and 7"],
      HARD: ["10 guesses", "6 digits", "Digits between 0 and 9"],
      IMPOSSIBLE: ["5 guesses", "10 digits", "Digits between 0 and 9"],
  }

  const handleGuess = async () => {
      try {
          const response = await fetch('http://127.0.0.1:5000/submit-guess', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ guess: guess }),
          });

          if (!response.ok) {
              throw new Error(`Failed to submit guess: ${response.statusText}`);
          }

          const result = await response.json();
          console.log(result);

          setCorrectNumbers(result.correctNumbers);
          setCorrectPositions(result.correctPositions);
          setRemainingGuesses(result.remainingGuesses);
          // navigate("/mastermind", { state: { difficulty: mode } });
      } catch (error) {
          console.error('Error submitting guess:', error.message);
          alert('Failed to submit guess, please try again.');
      }
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
        <h4 className="game-text">{correctNumbers} correct numbers and {correctPositions} correct positions</h4>
        <input
            type="text"
            value={guess}
            onChange={(e) => setGuess(e.target.value)}
            placeholder="Enter your guess"
            className="guess-input"
        />
        <button className="guess-button" onClick={handleGuess}>Guess</button>
        {remainingGuesses !== null && (
            <h4 className="game-text">{remainingGuesses} guesses remaining</h4>
        )}
    </div>
  );
};

export default Mastermind;
