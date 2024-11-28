import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './CreateAccount.css';

const CreateAccount = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleCreate = async (e) => {
      e.preventDefault();
      if (!username || !password) {
          console.error('Username and password are required');
          return;
      }

      if (password.length < 8) {
          alert('Password must be at least 8 characters');
          return;
      }

      try {
          const response = await fetch('http://127.0.0.1:5000/create-user', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ username, password }),
          });

          if (response.ok) {
              navigate("/difficulty-selector");
          } else {
              const errorDetail = await response.json();
              console.error('Failed to create account:', errorDetail.detail || 'Unknown error');
          }
      } catch (error) {
          console.error('Error:', error.message);
      }
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
              onChange={(e) => setUsername(e.target.value.trim())}
              required
          />
          <input
              type="password"
              className="pw-input-field"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value.trim())}
              required
          />
          <button className="create-button" type="submit">Create</button>
          </form>
      </div>
  );
};

export default CreateAccount;
