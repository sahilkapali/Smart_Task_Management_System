import { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('access'));

  const login = (accessToken, refreshToken) => {
    localStorage.setItem('access', accessToken);
    localStorage.setItem('refresh', refreshToken);
    setToken(accessToken);
  };

  const logout = () => {
    localStorage.clear();
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);