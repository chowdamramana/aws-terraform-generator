import React, { useState } from 'react';
import axios from 'axios';

const TerraformOutput = ({ configs }) => {
  const [selectedConfig, setSelectedConfig] = useState('');
  const [output, setOutput] = useState('');
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    try {
      const res = await axios.post(`/config/${selectedConfig}/terraform`);
      setOutput(res.data.content);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate Terraform code');
    }
  };

  const handleDownload = () => {
    const blob = new Blob([output], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'main.tf';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-2xl mb-4">Generate Terraform Code</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="mb-4">
        <label className="block mb-1">Select Config</label>
        <select
          value={selectedConfig}
          onChange={(e) => setSelectedConfig(e.target.value)}
          className="w-full border p-2 rounded"
        >
          <option value="">Select</option>
          {configs.map((config) => (
            <option key={config.id} value={config.id}>{config.name}</option>
          ))}
        </select>
      </div>
      <button
        onClick={handleGenerate}
        className="bg-blue-500 text-white p-2 rounded mr-2"
        disabled={!selectedConfig}
      >
        Generate
      </button>
      {output && (
        <>
          <pre className="bg-gray-100 p-4 rounded mb-4">{output}</pre>
          <button
            onClick={handleDownload}
            className="bg-green-500 text-white p-2 rounded"
          >
            Download
          </button>
        </>
      )}
    </div>
  );
};

export default TerraformOutput;