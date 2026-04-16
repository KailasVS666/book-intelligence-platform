"use client";
import { useState, useEffect } from 'react';
import BookGrid from './components/BookGrid';

export default function Dashboard() {
  const [books, setBooks] = useState([]);
  const [filteredBooks, setFilteredBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("All");

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/books/');
        const data = await response.json();
        setBooks(data);
        setFilteredBooks(data);
      } catch (error) {
        console.error("Error fetching books:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchBooks();
  }, []);

  useEffect(() => {
    let result = books;
    
    if (searchTerm) {
      result = result.filter(book => 
        book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (book.author && book.author.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }
    
    if (selectedGenre !== "All") {
      result = result.filter(book => book.genre === selectedGenre);
    }
    
    setFilteredBooks(result);
  }, [searchTerm, selectedGenre, books]);

  const genres = ["All", ...new Set(books.map(b => b.genre).filter(Boolean))];

  return (
    <main className="min-h-screen p-8 max-w-7xl mx-auto">
      <header className="mb-12 space-y-4">
        <h1 className="text-5xl font-extrabold tracking-tight gradient-text">
          Document Intelligence
        </h1>
        <p className="text-gray-400 text-lg max-w-2xl">
          Interact with books using AI. Explore summaries, sentiment, and ask questions through our RAG-enhanced pipeline.
        </p>
      </header>

      <div className="flex flex-col md:flex-row gap-4 mb-10 items-center">
        <div className="relative flex-grow w-full">
          <input
            type="text"
            placeholder="Search by title or author..."
            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <svg className="absolute right-4 top-3.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        
        <select 
          className="bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all w-full md:w-48 appearance-none"
          value={selectedGenre}
          onChange={(e) => setSelectedGenre(e.target.value)}
        >
          {genres.map(genre => (
            <option key={genre} value={genre} className="bg-black text-white">{genre}</option>
          ))}
        </select>
      </div>

      <BookGrid books={filteredBooks} loading={loading} />
    </main>
  );
}
