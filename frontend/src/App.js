import React, { useState, createContext, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import TenantPortal from './components/TenantPortal';
import MobileHomeManager from './components/MobileHomeManager';

export const AuthContext = createContext();

const App = () => {
  const [token, setToken] = useState('');

  const login = async (email, password) => {
    const res = await axios.post('/api/login', { email, password });
    setToken(res.data.token);
  };

  return (
    <AuthContext.Provider value={{ token, login }}>
      <Router>
        <nav style={{ 
          padding: '10px', 
          backgroundColor: '#f8f9fa', 
          borderBottom: '1px solid #dee2e6',
          marginBottom: '20px'
        }}>
          <Link to="/" style={{ marginRight: '20px', textDecoration: 'none' }}>Dashboard</Link>
          <Link to="/tenant" style={{ marginRight: '20px', textDecoration: 'none' }}>Tenant Portal</Link>
          <Link to="/mobile-homes" style={{ marginRight: '20px', textDecoration: 'none' }}>Mobile Home VIN Recovery</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/tenant" element={<TenantPortal />} />
          <Route path="/mobile-homes" element={<MobileHomeManager />} />
        </Routes>
      </Router>
    </AuthContext.Provider>
  );
};

export default App;
