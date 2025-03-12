import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignUp from './pages/SignUp/SignUpPage';
import MainPage from './pages/MainPage/MainPage';
import LoginPage from './pages/LoginPage/LoginPage';
import PrivateRoute from './components/PrivateRoute';
import ConfirmSignUp from './pages/ConfirmSignUpPage/ConfirmSignUpPage';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <>
    <div>
      <h1>Nickname Validator</h1>
      <Routes> {/* Define routes for the pages */}
          <Route path="/" element={
              <PrivateRoute>
                <MainPage />
              </PrivateRoute>
            } />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/confirm-signup" element={<ConfirmSignUp />} />
      </Routes>
    </div>
  </>
  );
}

export default App;
