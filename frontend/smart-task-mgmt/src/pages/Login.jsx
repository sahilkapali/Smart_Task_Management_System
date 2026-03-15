import { useState } from 'react';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [creds, setCreds] = useState({ username: '', password: '' });
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // NOTE: Ensure this matches your baseURL logic. 
      // If baseURL is '.../api/', then 'users/auth/login/' is correct.
      const res = await api.post('users/auth/login/', creds);
      
      // Successfully accessing the nested tokens from your Django View
      if (res.data.tokens) {
        login(res.data.tokens.access, res.data.tokens.refresh);
        navigate('/dashboard');
      }
    } catch (err) {
      // This will now show you the SPECIFIC error from your Serializer
      const errorMsg = err.response?.data?.non_field_errors?.[0] || 
                       err.response?.data?.detail || 
                       "Login failed. Check your connection.";
      alert("Error: " + errorMsg);
      console.error("Login Detail:", err.response?.data);
    }
  };

  return (
    <div className="auth-form">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px', textAlign: 'left' }}>
          <label>Username</label>
          <input 
            type="text" 
            value={creds.username}
            onChange={e => setCreds({...creds, username: e.target.value})} 
            required 
          />
        </div>
        <div style={{ marginBottom: '15px', textAlign: 'left' }}>
          <label>Password</label>
          <input 
            type="password" 
            value={creds.password}
            onChange={e => setCreds({...creds, password: e.target.value})} 
            required 
          />
        </div>
        <button type="submit">Sign In</button>
      </form>
      <p style={{ marginTop: '15px' }}>
        Need an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}