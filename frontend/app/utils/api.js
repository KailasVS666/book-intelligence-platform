const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`API Error [${endpoint}]:`, error.message);
    throw error;
  }
}

export const booksApi = {
  getAll: () => apiRequest("/books/"),
  getById: (id) => apiRequest(`/books/${id}/`),
  getRecommendations: (id) => apiRequest(`/books/${id}/recommendations/`),
  askQuestion: (data) => apiRequest("/books/ask/", {
    method: "POST",
    body: JSON.stringify(data),
  }),
};
