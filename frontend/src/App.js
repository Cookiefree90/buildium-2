import React, { useState, createContext, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import TenantPortal from './components/TenantPortal';

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
        <nav>
          <Link to="/">Dashboard</Link> | <Link to="/tenant">Tenant Portal</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/tenant" element={<TenantPortal />} />
        </Routes>
      </Router>
    </AuthContext.Provider>
  );
};

export default App;
