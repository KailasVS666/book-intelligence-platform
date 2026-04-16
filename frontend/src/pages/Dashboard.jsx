import React, { useEffect, useState } from 'react';
import { getBooks } from '../services/api';
import { Link } from 'react-router-dom';
import { Book as BookIcon, Star, Tag, ChevronRight, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

const Dashboard = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      const res = await getBooks();
      setBooks(res.data);
    } catch (err) {
      setError('Failed to fetch books. Is the backend running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
      <Loader2 className="w-10 h-10 text-primary-500 animate-spin" />
      <p className="text-slate-400 animate-pulse">Scanning library...</p>
    </div>
  );

  if (error) return (
    <div className="glass-card border-red-500/30 text-center py-12 max-w-lg mx-auto mt-10">
      <p className="text-red-400 mb-4">{error}</p>
      <button onClick={fetchBooks} className="btn-primary">Try Again</button>
    </div>
  );

  return (
    <div className="space-y-10">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            Book Intelligence
          </h1>
          <p className="text-slate-400 mt-2 text-lg">
            Discover insights from your personal collection of {books.length} books.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {books.map((book, index) => (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            key={book.id}
          >
            <Link to={`/book/${book.id}`} className="glass-card group flex flex-col h-full">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-primary-950/50 rounded-xl group-hover:bg-primary-600/20 transition-colors">
                  <BookIcon className="w-6 h-6 text-primary-400" />
                </div>
                <div className="flex items-center gap-1 bg-slate-900 px-3 py-1 rounded-full text-xs font-semibold text-amber-400">
                  <Star className="w-3 h-3 fill-current" />
                  {book.rating || 'N/A'}
                </div>
              </div>
              
              <h3 className="text-xl font-bold mb-1 group-hover:text-primary-400 transition-colors">
                {book.title}
              </h3>
              <p className="text-slate-400 text-sm mb-4 italic">by {book.author}</p>
              
              {book.summary && (
                <p className="text-slate-300 text-sm line-clamp-3 mb-6 flex-grow leading-relaxed">
                  {book.summary}
                </p>
              )}

              <div className="flex items-center justify-between mt-auto">
                <span className="flex items-center gap-1.5 text-xs font-medium text-slate-500 bg-slate-900/50 px-3 py-1.5 rounded-lg">
                  <Tag className="w-3 h-3" />
                  {book.genre || 'General'}
                </span>
                <span className="text-primary-400 text-sm font-semibold flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
                  Details <ChevronRight className="w-4 h-4" />
                </span>
              </div>
            </Link>
          </motion.div>
        ))}
        {books.length === 0 && (
            <div className="col-span-full py-20 text-center glass-card">
                <p className="text-slate-500 text-lg">No books found in the library.</p>
            </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
