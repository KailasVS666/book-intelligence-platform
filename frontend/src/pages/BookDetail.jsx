import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getBook, getRecommendations } from '../services/api';
import { ChevronLeft, Star, Tag, Link as LinkIcon, Sparkles, Loader2, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

const BookDetail = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [bookRes, recRes] = await Promise.all([
        getBook(id),
        getRecommendations(id)
      ]);
      setBook(bookRes.data);
      setRecommendations(recRes.data);
    } catch (err) {
      setError('Failed to load book details.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <Loader2 className="w-10 h-10 text-primary-500 animate-spin" />
    </div>
  );

  if (error || !book) return (
    <div className="text-center py-20">
      <p className="text-red-400 mb-6 font-medium">{error || 'Book not found'}</p>
      <Link to="/" className="btn-primary inline-flex items-center gap-2">
        <ChevronLeft className="w-4 h-4" /> Back to Library
      </Link>
    </div>
  );

  return (
    <div className="max-w-5xl mx-auto space-y-12 pb-20">
      <Link to="/" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
        <ChevronLeft className="w-4 h-4" /> Back to Library
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        {/* Main Details */}
        <div className="lg:col-span-2 space-y-8">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-4"
          >
            <div className="flex flex-wrap items-center gap-3">
              <span className="bg-primary-600/20 text-primary-400 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border border-primary-500/20">
                {book.genre || 'General'}
              </span>
              <div className="flex items-center gap-1.5 text-amber-400 font-bold bg-amber-400/10 px-3 py-1 rounded-full text-sm">
                <Star className="w-4 h-4 fill-current" />
                {book.rating || 'N/A'}
              </div>
            </div>
            <h1 className="text-5xl font-extrabold tracking-tight text-white leading-tight">
              {book.title}
            </h1>
            <p className="text-2xl text-slate-400 font-medium">by {book.author}</p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="glass-card bg-slate-900/40"
          >
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary-400" />
              Intelligence Summary
            </h2>
            <p className="text-slate-300 leading-relaxed text-lg italic">
              "{book.summary || 'Summary not available yet.'}"
            </p>
          </motion.div>

          <div className="space-y-4">
            <h3 className="text-xl font-bold text-slate-200">Full Description</h3>
            <p className="text-slate-400 leading-loose text-lg whitespace-pre-line">
              {book.description || 'No description provided.'}
            </p>
          </div>
          
          <div className="pt-6 border-t border-slate-800">
             <a 
              href={book.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 font-semibold transition-colors group"
             >
                <LinkIcon className="w-4 h-4" /> View Original Source <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
             </a>
          </div>
        </div>

        {/* Recommendations Sidebar */}
        <div className="space-y-6">
          <h3 className="text-xl font-bold flex items-center gap-2 px-2">
            Similar Reads
          </h3>
          <div className="space-y-4">
            {recommendations.length > 0 ? recommendations.map((rec, i) => (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * i }}
                key={rec.id}
              >
                <Link to={`/book/${rec.id}`} className="glass-card !p-4 flex gap-4 items-center group">
                  <div className="w-12 h-16 bg-slate-800 rounded flex items-center justify-center shrink-0">
                     <Tag className="w-5 h-5 text-slate-600" />
                  </div>
                  <div className="min-w-0">
                    <h4 className="font-bold text-slate-200 truncate group-hover:text-primary-400 transition-colors">
                      {rec.title}
                    </h4>
                    <p className="text-sm text-slate-500 truncate">{rec.author}</p>
                  </div>
                </Link>
              </motion.div>
            )) : (
              <p className="text-slate-500 text-center italic py-10 glass-card">
                No similar books found in the collection.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookDetail;
