import { useState } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

export default function Register() {
  const [form, setForm] = useState({ 
    username: '', 
    email: '', 
    password: '', 
    password2: '' 
  });
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    
    // Quick local check
    if (form.password !== form.password2) {
      alert("Passwords do not match!");
      return;
    }

    try {
      // Added a trailing slash to be safe
      await api.post('users/auth/register/', form);
      alert("Account Created successfully! You can now login.");
      navigate('/login');
    } catch (err) {
      // Capture the specific error from Django
      const errorData = err.response?.data;
      let errorMessage = "Registration failed.";

      if (errorData) {
        // Formats errors like "username: This username is already taken"
        errorMessage = Object.keys(errorData)
          .map(key => `${key}: ${errorData[key]}`)
          .join("\n");
      }
      
      alert(errorMessage);
      console.error("Registration detail:", errorData);
    }
  };

  return (
    <div className="auth-form">
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <div className="input-group">
          <label>Username</label>
          <input 
            placeholder="Username" 
            onChange={e => setForm({...form, username: e.target.value})} 
            required 
          />
        </div>
        <div className="input-group">
          <label>Email</label>
          <input 
            placeholder="Email" 
            type="email" 
            onChange={e => setForm({...form, email: e.target.value})} 
            required 
          />
        </div>
        <div className="input-group">
          <label>Password</label>
          <input 
            placeholder="Minimum 8 characters" 
            type="password" 
            onChange={e => setForm({...form, password: e.target.value})} 
            required 
          />
        </div>
        <div className="input-group">
          <label>Confirm Password</label>
          <input 
            placeholder="Confirm Password" 
            type="password" 
            onChange={e => setForm({...form, password2: e.target.value})} 
            required 
          />
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}