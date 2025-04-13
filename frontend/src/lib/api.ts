import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export const fetchModules = async () => {
  const response = await api.get("/modules");
  return response.data;
};

export const createConfig = async (config: any) => {
  const response = await api.post("/config", config);
  return response.data;
};

export const fetchConfig = async (id: string) => {
  const response = await api.get(`/config/${id}`);
  return response.data;
};

export const generateTerraform = async (configId: string) => {
  const response = await api.get(`/preview/${configId}`);
  return response.data;
};

export default api;