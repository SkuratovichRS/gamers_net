const API_URL = 'http://localhost:8000/api/v1';

async function handleRequest(url, options) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        return response;
    } catch (error) {
        console.error('Network error:', error);
        throw new Error('Network error occurred. Please check your connection.');
    }
}

export async function getUserGames() {
    return handleRequest(`${API_URL}/games`, {
        method: 'GET',
        credentials: 'include'
    });
}

export async function addUserGame(gameName) {
    return handleRequest(`${API_URL}/games`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify({ name: gameName })
    });
}
