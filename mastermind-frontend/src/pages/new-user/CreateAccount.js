import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './CreateAccount.css';

const CreateAccount = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleCreate = (e) => {
      // Handle form submission
      // Send data to API
      console.log(username, password);
      navigate("/difficulty-selector");  // Navigate to next page after form submission
    };


    return (
      <div className="create-account-container">
          <h1 className="create-account-text">Create Account</h1>
          <form onSubmit={handleCreate}>
          <input
              type="text"
              className="user-input-field"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
          />
          <input
              type="text"
              className="pw-input-field"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
          />
          <button className="create-button" type="submit">Create</button>
          </form>
      </div>
  );
};

export default CreateAccount;
