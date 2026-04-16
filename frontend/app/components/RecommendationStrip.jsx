import BookCard from './BookCard';

export default function RecommendationStrip({ books }) {
  if (!books || books.length === 0) return null;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold gradient-text">Recommended For You</h2>
      <div className="flex overflow-x-auto pb-6 gap-6 scrollbar-hide snap-x">
        {books.map((book) => (
          <div key={book.id} className="min-w-[280px] max-w-[280px] snap-start">
            <BookCard book={book} />
          </div>
        ))}
      </div>
    </div>
  );
}
