import { createContext, useState, useEffect, useCallback } from "react";
import { loginAPI, refreshTokenAPI, logoutAPI } from "../utils/api";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(() => {
        if (typeof window !== "undefined") {
            return localStorage.getItem("user") || null;
        }
        return null;
    });

    const login = async (username, password) => {
        try {
            const data = await loginAPI(username, password);
            setIsAuthenticated(true);
            setUser(data.username);
            localStorage.setItem("user", data.username);
        } catch (error) {
            console.error("Ошибка при входе:", error);
        }
    };

    const logout = async () => {
        try {
            await logoutAPI();
            setIsAuthenticated(false);
            setUser(null)
            localStorage.removeItem("user");
        } catch (error) {
            console.error("Ошибка при выходе:", error);
        }
    };

    const refreshAccessToken = useCallback(async () => {
        try {
            await refreshTokenAPI();
            setIsAuthenticated(true);
        } catch (error) {
            console.error("Ошибка обновления токена:", error);
            setIsAuthenticated(false);
            setUser(null)
            localStorage.removeItem("user");
        }
    }, []);

    useEffect(() => {
        refreshAccessToken();
    }, [refreshAccessToken]);

    // Обновляем токен каждые 4 минуты
    useEffect(() => {
        const interval = setInterval(refreshAccessToken, 4 * 60 * 1000);
        return () => clearInterval(interval);
    }, [refreshAccessToken]);

    return (
        <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
