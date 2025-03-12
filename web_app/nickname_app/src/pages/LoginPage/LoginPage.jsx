import React, { useState, useContext } from "react";
import { useNavigate } from 'react-router-dom';
import { AuthenticateUser } from "../../auth/Login";
import "../AuthPages.css";
import { AuthContext } from "../../AuthProvider";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useContext(AuthContext)
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const user = await AuthenticateUser(email, password);
      console.log(user)
      login(user['session']['idToken']['jwtToken']);
      navigate('/');
    } catch (error) {
      setError(error.message);
    }
  };

  const handleConfirmSignUpRedirect = () => {
    // Redirect to Login page (assumes you have routing in place)
    navigate('/confirm-signup');
  };

  const handleSignUpRedirect = () => {
    // Redirect to Login page (assumes you have routing in place)
    navigate('/signup');
  };

  return (
    <div className="signup-container">
      <h2>Sign in</h2>
      {error && <p className="error">{error}</p>}

      <form onSubmit={handleSubmit} className="form">
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Sign in</button>
      </form>
      <div className="links">
        <p>Signed up but didn't confirm your email?</p>
        <button onClick={handleConfirmSignUpRedirect}>Confirm Sign Up</button>
      </div>

      <div className="links">
        <p>Don't have an account?</p>
        <button onClick={handleSignUpRedirect}>Sign up</button>
      </div>
    </div>
  );
};

export default LoginPage;
