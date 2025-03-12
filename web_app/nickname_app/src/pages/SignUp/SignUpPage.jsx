import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import signUp from "../../auth/SignUp";
import "../AuthPages.css";

const SignUpPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signUp(email, email ,password ,{email});
      alert("Sign Up successful! Please check your email for confirmation.");
      navigate('/confirm-signup', { state: { email } });
    } catch (error) {
      setError(error.message);
    }
  };

  const handleConfirmSignUpRedirect = () => {
    // Redirect to Login page (assumes you have routing in place)
    navigate('/confirm-signup');
  };

  const handleLoginRedirect = () => {
    // Redirect to Login page (assumes you have routing in place)
    navigate('/login');
  };

  return (
    <div className="signup-container">
      <h2>Sign Up</h2>
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
        <button type="submit">Sign Up</button>
      </form>
      <div className="links">
        <p>If you already signed up please confirm your sign up</p>
        <button onClick={handleConfirmSignUpRedirect}>Confirm Sign Up</button>
      </div>

      <div className="links">
        <p>Already have an account?</p>
        <button onClick={handleLoginRedirect}>Login</button>
      </div>
    </div>
  );
};

export default SignUpPage;
