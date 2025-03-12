import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom'; // Import BrowserRouter for routing
import App from './App.jsx';
import './index.css';
import { AuthProvider } from './AuthProvider.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <Router> {/* Wrap the App with BrowserRouter */}
        <App />
      </Router>
    </AuthProvider>
  </StrictMode>,
);
