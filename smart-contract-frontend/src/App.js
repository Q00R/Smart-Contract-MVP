import './App.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'; // Update import
import Home from './pages/Home/Home';
import Login from './pages/Login/Login';
import Signup from './pages/Signup/Signup';
import Dashboard from './pages/Dashboard/Dashboard';
import React, { useEffect } from 'react';
import Cookies from 'js-cookie';

function App() {
  useEffect(() => {
    // Check if the token exists in cookies or local storage
    const token = Cookies.get('token'); // You can replace 'token' with your actual token key
    // const token = localStorage.getItem('token'); // Alternatively, use local storage

    // If token doesn't exist, you can use the <Navigate /> component to redirect
    if (!token) {
      return <Navigate to="/login" />;
    }
  }, []); // Empty dependency array to run the effect only once

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
