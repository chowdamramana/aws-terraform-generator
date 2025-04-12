import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ResourceForm = ({ resourceTypes, refreshConfigs }) => {
  const [resourceType, setResourceType] = useState('');
  const [properties, setProperties] = useState([]);
  const [formData, setFormData] = useState({ region: 'us-east-1', resources: [] });
  const [error, setError] = useState('');

  useEffect(() => {
    if (resourceType) {
      fetchProperties();
    }
  }, [resourceType]);

  const fetchProperties = async () => {
    try {
      const res = await axios.get(`/api/properties/${resourceType}`);
      setProperties(res.data);
      setFormData((prev) => ({
        ...prev,
        resources: [{
          resource_type: resourceType,
          properties: res.data.reduce((acc, p) => ({ ...acc, [p.name]: '' }), {}),
        }],
      }));
    } catch (err) {
      setError('Failed to fetch properties');
    }
  };

  const handlePropertyChange = (name, value) => {
    setFormData((prev) => ({
      ...prev,
      resources: [{
        resource_type: resourceType,
        properties: { ...prev.resources[0].properties, [name]: value },
      }],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/config', formData);
      refreshConfigs();
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save config');
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow mb-6">
      <h2 className="text-2xl mb-4">Create Configuration</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block mb-1">Region</label>
          <select
            value={formData.region}
            onChange={(e) => setFormData({ ...formData, region: e.target.value })}
            className="w-full border p-2 rounded"
          >
            <option value="us-east-1">us-east-1</option>
            <option value="us-west-2">us-west-2</option>
            <option value="eu-west-1">eu-west-1</option>
          </select>
        </div>
        <div className="mb-4">
          <label className="block mb-1">Resource Type</label>
          <select
            value={resourceType}
            onChange={(e) => setResourceType(e.target.value)}
            className="w-full border p-2 rounded"
          >
            <option value="">Select Resource</option>
            {resourceTypes.map((rt) => (
              <option key={rt} value={rt}>{rt}</option>
            ))}
          </select>
        </div>
        {properties.map((prop) => (
          <div key={prop.name} className="mb-4">
            <label className="block mb-1">{prop.name} {prop.required && '*'}</label>
            {prop.type === 'select' ? (
              <select
                value={formData.resources[0]?.properties[prop.name] || ''}
                onChange={(e) => handlePropertyChange(prop.name, e.target.value)}
                className="w-full border p-2 rounded"
                required={prop.required}
              >
                <option value="">Select</option>
                {prop.options.map((opt) => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            ) : prop.type === 'checkbox' ? (
              <input
                type="checkbox"
                checked={formData.resources[0]?.properties[prop.name] === 'true'}
                onChange={(e) => handlePropertyChange(prop.name, e.target.checked.toString())}
                className="h-5 w-5"
              />
            ) : (
              <input
                type="text"
                value={formData.resources[0]?.properties[prop.name] || ''}
                onChange={(e) => handlePropertyChange(prop.name, e.target.value)}
                className="w-full border p-2 rounded"
                required={prop.required}
              />
            )}
            <p className="text-sm text-gray-500">{prop.description}</p>
          </div>
        ))}
        <button type="submit" className="bg-blue-500 text-white p-2 rounded">
          Save Config
        </button>
      </form>
    </div>
  );
};

export default ResourceForm;