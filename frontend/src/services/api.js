import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getBooks = () => api.get('books/');
export const getBook = (id) => api.get(`books/${id}/`);
export const getRecommendations = (id) => api.get(`books/${id}/recommend/`);
export const uploadBook = (data) => api.post('books/upload/', data);
export const askQuestion = (question) => api.post('ask/', { question });

export default api;
