"use client";
import QABox from '../components/QABox';
import Link from 'next/link';

export default function GlobalAsk() {
  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto space-y-12">
      <Link href="/" className="inline-flex items-center text-gray-400 hover:text-white transition-colors gap-2 group">
        <svg className="w-5 h-5 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Dashboard
      </Link>

      <div className="space-y-4 text-center">
        <h1 className="text-4xl font-extrabold tracking-tight gradient-text">
          Global Knowledge Base
        </h1>
        <p className="text-gray-400 text-lg">
          Ask anything about our entire library. The AI will search through all indexed book chunks to find citations and answers.
        </p>
      </div>

      <div className="mt-12">
        <QABox bookId={null} />
      </div>

      <div className="pt-12 border-t border-white/10">
        <h3 className="text-sm font-bold text-gray-500 uppercase tracking-widest mb-6">Suggested Questions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            "Which books are about magic and wizardry?",
            "Can you suggest a book with a positive and uplifting tone?",
            "What is the most common theme in our library?",
            "Summarize the general sentiment of the books available."
          ].map((q, i) => (
            <div key={i} className="glass-card p-4 text-sm text-gray-400 cursor-pointer hover:text-purple-300 transition-colors">
              "{q}"
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
