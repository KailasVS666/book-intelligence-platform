import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import BookDetail from './pages/BookDetail';
import AskQuestion from './pages/AskQuestion';
import { BookOpen, Search, LayoutDashboard, PlusCircle } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;

  return (
    <nav className="border-b border-slate-800 bg-slate-950/50 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <div className="bg-primary-600 p-1.5 rounded-lg group-hover:rotate-12 transition-transform">
            <BookOpen className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight">BookIntel</span>
        </Link>
        
        <div className="flex items-center gap-8">
          <Link to="/" className={`nav-link flex items-center gap-2 ${isActive('/') ? 'text-white' : ''}`}>
            <LayoutDashboard className="w-4 h-4" /> Dashboard
          </Link>
          <Link to="/ask" className={`nav-link flex items-center gap-2 ${isActive('/ask') ? 'text-white' : ''}`}>
            <Search className="w-4 h-4" /> Ask AI
          </Link>
          <button className="btn-primary flex items-center gap-2 !px-4 !py-1.5 text-sm">
            <PlusCircle className="w-4 h-4" /> Upload
          </button>
        </div>
      </div>
    </nav>
  );
};

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-grow max-w-7xl mx-auto px-4 py-8 w-full">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/book/:id" element={<BookDetail />} />
            <Route path="/ask" element={<AskQuestion />} />
          </Routes>
        </main>
        
        <footer className="border-t border-slate-900 py-8 text-center text-slate-600 text-sm">
          <p>© 2026 Book Intelligence Platform • Powered by Gemini & Sentence Transformers</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
