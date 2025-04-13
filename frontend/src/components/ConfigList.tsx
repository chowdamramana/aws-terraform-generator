import * as React from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { Config } from "@/types";

const ConfigList: React.FC = () => {
  const { data: configs, isLoading } = useQuery<Config[]>({
    queryKey: ["configs"],
    queryFn: async () => {
      const res = await api.get("/config");
      return res.data;
    },
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="p-4">
      <h2 className="text-2xl mb-4">Your Configurations</h2>
      {configs?.length ? (
        <ul className="space-y-2">
          {configs.map((config) => (
            <li key={config.id}>
              <Link to={`/preview/${config.id}`} className="text-blue-600 hover:underline">
                {config.name}
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No configurations found.</p>
      )}
    </div>
  );
};

export default ConfigList;