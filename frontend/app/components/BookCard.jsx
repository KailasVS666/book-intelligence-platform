import Link from 'next/link';

export default function BookCard({ book }) {
  const ratingStars = (rating) => {
    const stars = Math.round(rating || 0);
    return "★".repeat(stars) + "☆".repeat(5 - stars);
  };

  return (
    <Link href={`/books/${book.id}`} className="block">
      <div className="glass-card overflow-hidden h-full flex flex-col group">
        <div className="relative h-64 overflow-hidden bg-gray-900">
          <img 
            src={book.cover_image_url || 'https://via.placeholder.com/150x225?text=No+Cover'} 
            alt={book.title}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
          {book.genre && (
            <span className="absolute top-3 right-3 bg-purple-600/80 backdrop-blur-md text-white text-xs px-2 py-1 rounded-full border border-purple-400/30">
              {book.genre.split(',')[0].trim()}
            </span>
          )}

        </div>
        
        <div className="p-4 flex-grow flex flex-col">
          <h3 className="font-bold text-lg leading-tight mb-1 line-clamp-2 group-hover:text-purple-400 transition-colors">
            {book.title}
          </h3>
          <p className="text-gray-400 text-sm mb-2">{book.author || 'Unknown Author'}</p>
          
          <div className="mt-auto flex items-center justify-between">
            <div className="flex flex-col">
              <span className="text-yellow-500 text-sm font-medium">
                {ratingStars(book.rating)}
              </span>
              <span className="text-gray-500 text-xs">{book.review_count || 0} reviews</span>
            </div>
            <div className="text-purple-400 font-semibold">
              View AI Stats
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}
