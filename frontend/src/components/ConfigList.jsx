import React from 'react';

const ConfigList = ({ configs }) => {
  return (
    <div className="bg-white p-6 rounded shadow mb-6">
      <h2 className="text-2xl mb-4">Saved Configurations</h2>
      {configs.length === 0 ? (
        <p>No configurations found.</p>
      ) : (
        <ul>
          {configs.map((config) => (
            <li key={config.id} className="mb-2">
              <strong>{config.name}</strong> - {config.region} ({config.resources.length} resources)
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ConfigList;