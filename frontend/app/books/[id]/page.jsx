"use client";
import { useParams } from 'next/navigation';
import QABox from '../../components/QABox';
import RecommendationStrip from '../../components/RecommendationStrip';
import Link from 'next/link';
import { useBookDetail } from '../../hooks/useBooks';
import { DetailSkeleton } from '../../components/Skeleton';

export default function BookDetail() {
  const { id } = useParams();
  const { book, recommendations, loading, error } = useBookDetail(id);

  if (loading) return <main className="min-h-screen p-8 max-w-7xl mx-auto"><DetailSkeleton /></main>;
  if (error || !book) return <div className="p-8 text-center text-red-400">Error: {error || 'Book not found'}</div>;

  const sentimentColor = {
    'Positive': 'bg-green-500/20 text-green-400 border-green-500/30',
    'Neutral': 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    'Negative': 'bg-red-500/20 text-red-400 border-red-500/30',
    'Mixed': 'bg-orange-500/20 text-orange-400 border-orange-500/30'
  }[book.sentiment] || 'bg-gray-500/20 text-gray-400 border-gray-500/30';

  return (
    <main className="min-h-screen p-8 max-w-7xl mx-auto space-y-12 animate-in fade-in duration-700">
      <Link href="/" className="inline-flex items-center text-gray-400 hover:text-white transition-colors gap-2 group">
        <svg className="w-5 h-5 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Dashboard
      </Link>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
        <div className="md:col-span-1">
          <div className="glass-card overflow-hidden sticky top-8 group">
            <img 
              src={book.cover_image_url || 'https://via.placeholder.com/300x450'} 
              alt={book.title} 
              className="w-full h-auto transform transition-transform duration-500 group-hover:scale-105"
            />
          </div>
        </div>

        <div className="md:col-span-2 space-y-8">
          <div className="space-y-4">
            <h1 className="text-4xl font-black leading-tight gradient-text">{book.title}</h1>
            <p className="text-xl text-gray-400">by {book.author || 'Unknown Author'}</p>
            
            <div className="flex flex-wrap gap-3">
              {book.genre && book.genre.split(',').map((g, index) => (
                <span key={index} className="bg-purple-600/30 text-purple-300 border border-purple-500/30 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
                  {g.trim()}
                </span>
              ))}
              {book.sentiment && (
                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${sentimentColor}`}>
                  {book.sentiment} Tone
                </span>
              )}
              <span className="bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
                ★ {book.rating || 0} / 5
              </span>
            </div>
          </div>

          <section className="space-y-4">
            <h2 className="text-xl font-bold text-gray-200 border-b border-white/5 pb-2">Description</h2>
            <p className="text-gray-400 leading-relaxed">{book.description || 'No description available.'}</p>
          </section>

          {book.ai_summary && (
            <section className="glass-card p-6 bg-purple-900/10 border-purple-500/20 hover:border-purple-500/40 transition-colors">
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-purple-300">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10.394 2.813a1 1 0 00-.788 0l-7 3a1 1 0 000 1.841l3.394 1.455a1 1 0 001.037-.152L10 6.273l2.975 2.684a1 1 0 001.037.152l3.394-1.455a1 1 0 000-1.841l-7-3zM3 13.5a1 1 0 011-1h1.5a1 1 0 011 1v2.5a1 1 0 01-1 1H4a1 1 0 01-1-1v-2.5z" />
                </svg>
                AI Forensic Insights
              </h2>
              <p className="text-gray-300 leading-relaxed italic border-l-2 border-purple-500 pl-4 py-1">"{book.ai_summary}"</p>
            </section>
          )}

          <QABox bookId={book.pk || book.id} />
        </div>
      </div>

      <RecommendationStrip books={recommendations} />
    </main>
  );
}

