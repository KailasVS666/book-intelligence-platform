import { Inter } from "next/font/google";
import "./globals.css";
import Link from 'next/link';

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Document Intelligence Platform",
  description: "AI-powered book insights and Q&A",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="border-b border-white/10 bg-black/50 backdrop-blur-xl sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-8 h-16 flex items-center justify-between">
            <Link href="/" className="text-xl font-bold gradient-text">
              DocIntel
            </Link>
            <div className="flex gap-8">
              <Link href="/" className="text-sm text-gray-400 hover:text-white transition-colors">
                Dashboard
              </Link>
              <Link href="/ask" className="text-sm text-gray-400 hover:text-white transition-colors">
                Global Ask
              </Link>
            </div>
          </div>
        </nav>
        {children}
        <footer className="border-t border-white/10 py-12 mt-20">
          <div className="max-w-7xl mx-auto px-8 text-center text-gray-500 text-sm">
            © 2026 Document Intelligence Platform • Built for Ergosphere Solutions
          </div>
        </footer>
      </body>
    </html>
  );
}
