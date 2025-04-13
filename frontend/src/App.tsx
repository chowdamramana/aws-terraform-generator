import * as React from "react";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import Header from "./components/Header";
import ConfigList from "./components/ConfigList";
import ResourceWizard from "./components/ResourceWizard";
import TerraformPreview from "./components/TerraformPreview";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="min-h-screen">
        <Header />
        <Routes>
          <Route path="/" element={<ConfigList />} />
          <Route path="/wizard" element={<ResourceWizard />} />
          <Route path="/preview/:configId" element={<TerraformPreview />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;