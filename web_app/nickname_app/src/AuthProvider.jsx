import React, { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [idToken, setIdToken] = useState(() => localStorage.getItem("idToken"));
  const [isAuthenticated, setIsAuthenticated] = useState(!!idToken);

  const login = (token) => {
    localStorage.setItem("idToken", token);
    setIdToken(token);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem("idToken");
    setIdToken(null);
    setIsAuthenticated(false);
  };

  useEffect(() => {
    const token = localStorage.getItem("idToken");
    if (token) {
      setIdToken(token);
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ idToken, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
