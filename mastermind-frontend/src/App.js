import React from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import Welcome from "./pages/welcome/Welcome";
import CreateAccount from "./pages/new-user/CreateAccount";
import Difficulty from "./pages/difficulty-mode/DifficultyMode";
import Mastermind from "./pages/mastermind/Mastermind";
import SignIn from "./pages/sign-in/SignIn";
import GameOver from "./pages/game-over/GameOver";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/create-account" element={<CreateAccount />} />
        <Route path="/sign-in" element={<SignIn />} />
        <Route path="/difficulty-selector" element={<Difficulty />} />
        <Route path="/mastermind" element={<Mastermind />} />
        <Route path="/game-over" element={<GameOver />} />
      </Routes>
    </Router>
  );
};

export default App;
