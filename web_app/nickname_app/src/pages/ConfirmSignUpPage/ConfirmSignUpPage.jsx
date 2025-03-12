import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import { confirmSignUp } from "../../auth/ConfirmSignUp";
import "../AuthPages.css";

const ConfirmSignUpPage = () => {
  const [confirmationCode, setConfirmationCode] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await confirmSignUp(email, confirmationCode);
      alert("Your account has been confirmed! You can now sign in.");
      navigate('/login');
    } catch (error) {
      setError(error.message);
    }
  };
  // Use useLocation to access the passed state
  const location = useLocation();
  const passedEmail = location.state?.email;
  useEffect(() => {
    if (passedEmail) {
      setEmail(passedEmail); // Set the email from state if available
    }
  }, [passedEmail]);

  const handleSignUpRedirect = () => {
    // Redirect to Login page (assumes you have routing in place)
    navigate('/signup');
  };

  const handleLoginRedirect = () => {
    // Redirect to Login page (assumes you have routing in place)
    navigate('/login');
  };

  return (
    <div className="signup-container">
      <h2>Confirm Sign Up</h2>
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
          <label>Confirmation Code</label>
          <input
            type="text"
            value={confirmationCode}
            onChange={(e) => setConfirmationCode(e.target.value)}
            required
          />
        </div>
        <button type="submit">Confirm</button>
      </form>
      <div className="links">
        <p>Email is only sent if you signed up</p>
        <button onClick={handleSignUpRedirect}>Sign Up</button>
      </div>

      <div className="links">
        <p>Already have an account?</p>
        <button onClick={handleLoginRedirect}>Login</button>
      </div>
    </div>
  );
};

export default ConfirmSignUpPage;