import React from "react";
import { useNavigate } from "react-router-dom";
import './Welcome.css';

const Welcome = () => {
  const navigate = useNavigate();

  return (
    <div className="sign-in-container">
      <h1 className="welcome-text">Welcome to Mastermind!</h1>
        <div className="buttons-container">
          <button
              className="new-user-button"
              onClick={() => navigate("/create-account")}>
            New User
          </button>
          <button
              className="return-user-button"
              onClick={() => navigate("/sign-in")}>
            Returning User
          </button>
        </div>
    </div>
  );
};

export default Welcome;
