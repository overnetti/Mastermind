import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import './GameOver.css';

const GameOver = () => {
    const navigate = useNavigate();

    const handlePlayAgain = () => {
        // No API call needed? need to make sure this is treated like Play when signing in
        navigate("/difficulty-selector");
    }

    const handleExit = () => {
        // Log user out w/ API
        navigate("/");
    }

    return (
        <div className="game-over-container">
            <h1 className="game-over-text">Game Over</h1>
            <h2>You won/lost!</h2>
            <h3>Display the stats here and get it with a get endpoint</h3>
            <div className="buttons-container">
                <button
                    className="play-again-button"
                    onClick={() => navigate("/difficulty-selector")}>
                    Play Again
                </button>
                <button
                    className="exit-button"
                    onClick={handleExit}>
                    Exit
                </button>
            </div>
        </div>
    )
}

export default GameOver;