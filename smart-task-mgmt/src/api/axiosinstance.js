import axios from "axios";
import { getAccessToken } from "../utils/tokenStorage";
const api = axios.create({
baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
headers: { "Content-Type": "application/json" },
timeout: 10000,
});
// ■■ Request interceptor — attach JWT on every call ■■
api.interceptors.request.use(
(config) => {
const token = getAccessToken();
if (token) {
config.headers.Authorization = `Bearer ${token}`;
}
return config;
},
(error) => Promise.reject(error)
);
// ■■ Response interceptor — handle 401 globally ■■
api.interceptors.response.use(
(response) => response,
(error) => {
if (error.response?.status === 401) {
// Token expired — clear and redirect to login
localStorage.clear();
window.location.href = "/login";
}
return Promise.reject(error);
}
);
export default api;