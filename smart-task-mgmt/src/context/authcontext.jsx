import { createContext, useContext, useState } from "react";
import { saveTokens, clearTokens, getAccessToken } from "../utils/tokenStorage";
const AuthContext = createContext(null);
export function AuthProvider({ children }) {
// Initialise from localStorage so page refresh keeps user logged in
const [isAuthenticated, setIsAuthenticated] = useState(
() => Boolean(getAccessToken())
);
const [user, setUser] = useState(null);
const login = (accessToken, refreshToken, userData) => {
saveTokens(accessToken, refreshToken);
setIsAuthenticated(true);
setUser(userData);
};
const logout = () => {
clearTokens();
setIsAuthenticated(false);
setUser(null);
};
return (
<AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
{children}
</AuthContext.Provider>
);
}
// Custom hook — clean to use in any component
export const useAuth = () => useContext(AuthContext);