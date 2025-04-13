interface User {
  id: string | null;
  email: string;
}

export const useAuth = () => {
  return {
    user: { id: null, email: "guest" },
    loading: false,
    login: async () => {},
    logout: async () => {},
    register: async () => {},
  };
};