"use client";
import { useState } from 'react';
import { booksApi } from '../utils/api';

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    try {
      const data = await booksApi.askQuestion({ question, book_id: bookId });
      setAnswer(data);
    } catch (error) {
      setAnswer({ 
        answer: "Connection failed. Please ensure the backend and Ollama are running.",
        sources: [] 
      });
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="glass-card p-6 ring-1 ring-white/10">
      <h3 className="text-xl font-bold mb-4 gradient-text">Ask AI about {bookId ? 'this book' : 'any book'}</h3>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What are the main themes? / Is this a positive story?"
          className="w-full bg-black/40 border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all resize-none"
          rows="3"
        />
        <button 
          type="submit" 
          disabled={loading}
          className="btn-primary w-full disabled:opacity-50"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                 <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                 <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Thinking...
            </span>
          ) : "Ask Question"}
        </button>
      </form>

      {answer && (
        <div className="mt-8 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-white/5 rounded-xl p-5 border border-white/10">
            <h4 className="text-purple-400 font-semibold mb-2 flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              AI Answer
            </h4>
            <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">{answer.answer}</p>
          </div>

          {answer.sources && answer.sources.length > 0 && (
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-gray-400 uppercase tracking-wider px-1">Sources Citations</h4>
              {answer.sources.map((source, idx) => (
                <div key={idx} className="bg-white/5 rounded-lg p-3 border-l-2 border-purple-500 text-sm">
                  <span className="text-purple-300 font-medium block mb-1">{source.book_title}</span>
                  <p className="text-gray-400 italic">"...{source.chunk}..."</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
