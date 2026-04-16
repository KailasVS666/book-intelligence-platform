import React, { useState, useRef, useEffect } from 'react';
import { askQuestion } from '../services/api';
import { Send, User, Bot, Loader2, Sparkles, BookOpen } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const AskQuestion = () => {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', text: "Hello! I'm your Book Intelligence Assistant. Ask me anything about the books in your library. For example: 'What can I learn from Atomic Habits?'" }
  ]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    const userQ = question;
    setQuestion('');
    setMessages(prev => [...prev, { role: 'user', text: userQ }]);
    setLoading(true);

    try {
      const res = await askQuestion(userQ);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        text: res.data.answer,
        book: res.data.book,
        confidence: res.data.confidence
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', text: "Sorry, I had trouble connecting to the intelligence engine." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-12rem)] flex flex-col">
      <div className="flex items-center justify-between mb-6 px-4">
        <div>
            <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                <Sparkles className="w-8 h-8 text-primary-400" />
                Ask Your Library
            </h1>
            <p className="text-slate-400 mt-1">Semantic search and Q&A powered by AI.</p>
        </div>
      </div>

      <div 
        ref={scrollRef}
        className="flex-grow overflow-y-auto space-y-6 px-4 pb-10 scrollbar-hide"
      >
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              key={i}
              className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 shadow-lg ${
                msg.role === 'user' ? 'bg-primary-600' : 'bg-slate-800 border border-slate-700'
              }`}>
                {msg.role === 'user' ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-primary-400" />}
              </div>
              <div className={`max-w-[80%] space-y-2`}>
                <div className={`p-4 rounded-2xl shadow-sm leading-relaxed text-lg ${
                  msg.role === 'user' 
                    ? 'bg-primary-600/10 border border-primary-500/20 text-slate-100 rounded-tr-none' 
                    : 'bg-slate-900 border border-slate-800 text-slate-300 rounded-tl-none'
                }`}>
                  {msg.text}
                </div>
                
                {msg.book && msg.book !== 'None' && (
                  <motion.div 
                    initial={{ scale: 0.95, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="flex items-center gap-2 text-xs font-semibold text-primary-400 bg-primary-400/5 px-3 py-1.5 rounded-lg border border-primary-400/10 w-fit"
                  >
                    <BookOpen className="w-3 h-3" />
                    Source: {msg.book} • Confidence: {(msg.confidence * 100).toFixed(1)}%
                  </motion.div>
                )}
              </div>
            </motion.div>
          ))}
          {loading && (
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-slate-800 border border-slate-700 shadow-lg">
                <Bot className="w-5 h-5 text-primary-400" />
              </div>
              <div className="p-4 bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none">
                <Loader2 className="w-5 h-5 text-primary-500 animate-spin" />
              </div>
            </div>
          )}
        </AnimatePresence>
      </div>

      <div className="p-4 bg-slate-950/80 backdrop-blur-md sticky bottom-0 border-t border-slate-800/50">
        <form onSubmit={handleSubmit} className="relative max-w-3xl mx-auto">
          <input
            autoFocus
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about your books..."
            className="w-full bg-slate-900/80 border border-slate-700/50 rounded-2xl px-6 py-4 pr-16 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all text-white placeholder:text-slate-500 shadow-xl"
          />
          <button
            disabled={!question.trim() || loading}
            type="submit"
            className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-primary-600 hover:bg-primary-500 disabled:bg-slate-800 disabled:text-slate-600 text-white rounded-xl transition-all active:scale-90"
          >
            <Send className="w-6 h-6" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default AskQuestion;
