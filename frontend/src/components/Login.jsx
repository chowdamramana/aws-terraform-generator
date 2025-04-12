import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ setUser, setToken }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isRegister) {
        const res = await axios.post('/auth/register', { email, password });
        setUser(res.data);
        setError('');
      } else {
        const res = await axios.post('/auth/jwt/login', new URLSearchParams({
          username: email,
          password,
        }));
        setToken(res.data.access_token);
        setUser({ email });
        localStorage.setItem('token', res.data.access_token);
        setError('');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded shadow">
      <h2 className="text-2xl mb-4">{isRegister ? 'Register' : 'Login'}</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
        </div>
        <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
          {isRegister ? 'Register' : 'Login'}
        </button>
      </form>
      <p className="mt-4 text-center">
        {isRegister ? 'Already have an account?' : "Don't have an account?"}
        <button
          onClick={() => setIsRegister(!isRegister)}
          className="text-blue-500 ml-1"
        >
          {isRegister ? 'Login' : 'Register'}
        </button>
      </p>
    </div>
  );
};

export default Login;