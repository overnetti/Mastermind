import React, {useState, useEffect} from "react";
import {useLocation, useNavigate} from "react-router-dom";
import './GameOver.css';

const GameOver = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { status } = location.state || { status: "Unknown" };
    const { userId } = location.state || {};
    const [playerData, setPlayerData] = useState({});

    useEffect(() => {
        const fetchPlayerData = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/get-player-stats?userId=${userId}`, {
                    method: 'GET',
                });
                const result = await response.json();
                setPlayerData(result);
                console.log("PLAYER DATA: ", result);
            } catch (error) {
                console.error('Error fetching player data: ', error.message);
            }
        };

        fetchPlayerData();
    }, []);

    const handleLogout = async () => {
        try {
            await fetch("http://127.0.0.1:5000/reset", {
                method: "POST",
            });
            console.log("Game and Player reset successfully.");
            navigate("/");
        } catch (error) {
            console.error("Error resetting instances:", error.message);
        }
    };

    return (
        <div className="game-over-container">
            <h1 className="game-over-text">You {status}!</h1>
            <h2 className="player-stats-header">Player Stats &#x1F60F;</h2>
                <ul className="player-stats">
                    <li>You're level {playerData.currentLevel}</li>
                    <li>Your experience is {Math.round(playerData.currentXp)}/{Math.round(playerData.xpToNextLevel)}</li>
                    <li>Your highest score is {playerData.highestScore}</li>
                    <li>You've won {playerData.gamesWon} games</li>
                    <li>You win {playerData.winRate}% of the time</li>
                </ul>
            <div className="buttons-container">
                <button
                    className="play-again-button"
                    onClick={() => navigate("/difficulty-selector")}>
                    Play Again
                </button>
                <button
                    className="exit-button"
                    onClick={handleLogout}>
                    Log out
                </button>
            </div>
        </div>
    )
}

export default GameOver;