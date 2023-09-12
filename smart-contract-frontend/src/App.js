import './App.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home/Home';
import Login from './pages/Login/Login';
import Signup from './pages/Signup/Signup';
import Dashboard from './pages/Dashboard/Dashboard';
import ReviewDocument from './pages/ReviewDocument/ReviewDocument';
import React from 'react';
import Cookies from 'js-cookie';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/dashboard"
          element={
            // Check if the user is logged in, and if not, navigate to the login page
            Cookies.get('token') ? <Dashboard /> : <Navigate to="/login" />
          }
        />
        <Route path="*" element={<Home />} />
        <Route path="/review-share-doc/:sharedDocumentId" element={
          // Check if the user is logged in, and if not, navigate to the login page
          Cookies.get('token') ? <ReviewDocument /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
