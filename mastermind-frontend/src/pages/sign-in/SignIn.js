import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import './SignIn.css';

const SignIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSignIn = (e) => {
        // Send data to API
        // Handle sign in and authentication in API
        console.log(username, password);
        navigate("/difficulty-selector");  // Navigate to next page after form submission
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
                <button className="sign-in-button" type="submit">Let's Play!</button>
            </form>
        </div>
  );
};

export default SignIn;
