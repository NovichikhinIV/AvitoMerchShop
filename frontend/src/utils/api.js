const API_BASE_URL = "http://localhost:8080/api";

const request = async (endpoint, options = {}) => {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            credentials: "include", // Включаем куки в запрос
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
        });

        if (!response.ok) {
            // Логирование ошибки сервера
            const errorData = await response.json().catch(() => ({}));
            const errorMessage = errorData.errors || `Ошибка ${response.status}`;
            console.error(`Ошибка запроса на ${endpoint}: ${errorMessage}`);
            throw new Error(errorMessage);
        }
        return response.status !== 204 ? response.json() : null;
    } catch (error) {
        console.error(`API request error: ${error.message}`);
        throw error;
    }
};

export const loginAPI = async (username, password) => {
    const data = await request("/auth/", {
        method: "POST",
        body: JSON.stringify({ username, password }),
    });
    data['username'] = username
    return data;

};

export const refreshTokenAPI = async () => {
    const data = await request("/auth/refresh/", { 
        method: "POST"
    });
    return data;
};

export const logoutAPI = async () => {
    const data = await request("/auth/logout/", { 
        method: "POST"
    });
    return data;
};

export const sendCoinAPI = (toUser, amount) =>
    request("/sendCoin/", {
        method: "POST",
        body: JSON.stringify({ toUser, amount }),
    });

export const buyItemAPI = (itemId) =>
    request(`/buy/${itemId}/`, {
        method: "POST",
    });


export const getProductsAPI = () => request("/products/", {});

export const getInfoAPI = () => request("/info/", {});

