import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../App';
import { io } from 'socket.io-client';

const Dashboard = () => {
  const { token } = useContext(AuthContext);
  const [properties, setProperties] = useState([]);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    if (token) {
      axios.get('/api/properties', { headers: { Authorization: `Bearer ${token}` } })
        .then(res => setProperties(res.data));
      const socket = io();
      socket.on('maintenance_update', msg => {
        setNotifications(n => [...n, msg]);
      });
      return () => socket.disconnect();
    }
  }, [token]);

  return (
    <div>
      <h2>Dashboard</h2>
      <ul>
        {properties.map(p => <li key={p.id}>{p.address} ({p.type})</li>)}
      </ul>
      <h3>Notifications</h3>
      <ul>
        {notifications.map((n, i) => <li key={i}>{n.status} request #{n.id}</li>)}
      </ul>
    </div>
  );
};

export default Dashboard;
