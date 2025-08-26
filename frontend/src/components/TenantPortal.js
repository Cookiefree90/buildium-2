import React, { useContext, useState } from 'react';
import axios from 'axios';
import { AuthContext } from '../App';

const TenantPortal = () => {
  const { token } = useContext(AuthContext);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const askGPT = async () => {
    const res = await axios.post('/api/gpt', { question }, { headers: { Authorization: `Bearer ${token}` } });
    setAnswer(res.data.answer);
  };

  return (
    <div>
      <h2>Tenant Portal</h2>
      <textarea value={question} onChange={e => setQuestion(e.target.value)} />
      <button onClick={askGPT}>Ask</button>
      <p>{answer}</p>
    </div>
  );
};

export default TenantPortal;
