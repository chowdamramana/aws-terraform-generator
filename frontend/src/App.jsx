import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/Login';
import ResourceForm from './components/ResourceForm';
import ConfigList from './components/ConfigList';
import TerraformOutput from './components/TerraformOutput';

const App = () => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [configs, setConfigs] = useState([]);
  const [resourceTypes, setResourceTypes] = useState([]);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchConfigs();
      fetchResourceTypes();
    }
  }, [token]);

  const fetchConfigs = async () => {
    try {
      const res = await axios.get('/config');
      setConfigs(res.data);
    } catch (err) {
      console.error('Failed to fetch configs:', err);
    }
  };

  const fetchResourceTypes = async () => {
    try {
      const res = await axios.get('/api/resource-types');
      setResourceTypes(res.data);
    } catch (err) {
      console.error('Failed to fetch resource types:', err);
    }
  };

  const handleLogout = () => {
    setToken('');
    setUser(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-600 p-4 text-white flex justify-between">
        <h1 className="text-2xl">AWS Terraform Generator</h1>
        {user && (
          <button onClick={handleLogout} className="bg-red-500 px-4 py-2 rounded">
            Logout
          </button>
        )}
      </nav>
      <main className="container mx-auto p-4">
        {!user ? (
          <Login setUser={setUser} setToken={setToken} />
        ) : (
          <>
            <ResourceForm resourceTypes={resourceTypes} refreshConfigs={fetchConfigs} />
            <ConfigList configs={configs} />
            <TerraformOutput configs={configs} />
          </>
        )}
      </main>
    </div>
  );
};

export default App;