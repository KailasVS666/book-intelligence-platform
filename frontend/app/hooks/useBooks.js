import { useState, useEffect, useCallback } from 'react';
import { booksApi } from '../utils/api';

/**
 * Custom hook for managing the book library state.
 * Handles fetching, filtering, and searching logic.
 */
export function useBooks() {
  const [books, setBooks] = useState([]);
  const [filteredBooks, setFilteredBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBooks = useCallback(async () => {
    setLoading(true);
    try {
      const data = await booksApi.getAll();
      setBooks(data);
      setFilteredBooks(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch books');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchBooks();
  }, [fetchBooks]);

  const filterBooks = useCallback((searchTerm, genre) => {
    let result = books;
    
    if (searchTerm) {
      result = result.filter(book => 
        book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (book.author && book.author.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }
    
    if (genre !== "All") {
      result = result.filter(book => 
        book.genre && book.genre.toLowerCase().includes(genre.toLowerCase())
      );
    }
    
    setFilteredBooks(result);
  }, [books]);

  return { books, filteredBooks, loading, error, filterBooks, refresh: fetchBooks };
}

/**
 * Custom hook for fetching individual book details and recommendations.
 */
export function useBookDetail(id) {
  const [data, setData] = useState({ book: null, recommendations: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;

    const fetchData = async () => {
      setLoading(true);
      try {
        const [book, recommendations] = await Promise.all([
          booksApi.getById(id),
          booksApi.getRecommendations(id)
        ]);
        setData({ book, recommendations });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  return { ...data, loading, error };
}
