import * as React from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";

const Header: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <header className="bg-blue-600 text-white p-4 flex justify-between items-center">
      <Link to="/" className="text-xl font-bold">
        AWS Terraform Generator
      </Link>
      <nav>
        <Link to="/wizard" className="mr-4">
          Create Config
        </Link>
        <Button variant="ghost" onClick={handleLogout}>
          Logout
        </Button>
      </nav>
    </header>
  );
};

export default Header;