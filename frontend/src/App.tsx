import * as React from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import ConfigList from "./components/ConfigList";
import ResourceWizard from "./components/ResourceWizard";
import TerraformPreview from "./components/TerraformPreview";
import Login from "./components/Login";
import Register from "./components/Register";
import { useAuth } from "./hooks/useAuth";

const App: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;

  return (
    <div className="min-h-screen">
      {user && <Header />}
      <Routes>
        <Route path="/" element={user ? <ConfigList /> : <Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/wizard" element={user ? <ResourceWizard /> : <Login />} />
        <Route path="/preview/:configId" element={user ? <TerraformPreview /> : <Login />} />
      </Routes>
    </div>
  );
};

export default App;