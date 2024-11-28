import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import './SignIn.css';

const SignIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSignIn = async (e) => {
        e.preventDefault();
        if (!username || !password) {
            alert('Username and password are required');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/login', {
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
                console.error('Failed to login:', errorDetail.detail || 'Unknown error');
            }
        } catch (error) {
            console.error('Error:', error.message);
        }
    };


    return (
        <div className="sign-in-container">
            <h1 className="sign-in-text">Sign In</h1>
            <form onSubmit={handleSignIn}>
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
                <button className="sign-in-button" type="submit">Let's Play!</button>
            </form>
        </div>
  );
};

export default SignIn;
