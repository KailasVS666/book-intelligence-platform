import json
import requests
import os

def load_to_db():
    json_path = os.path.join(os.path.dirname(__file__), "books_raw.json")
    api_url = "http://localhost:8000/api/books/upload/"
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run the scraper first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        books = json.load(f)

    print(f"Loading {len(books)} books to database via API...")
    
    success_count = 0
    error_count = 0

    for book in books:
        # Map rating text to float if needed on client side or handle in backend
        # The brief says rating is FloatField
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating_val = rating_map.get(book.get("rating_text"), 0)

        payload = {
            "title": book["title"],
            "author": book["author"],
            "rating": rating_val,
            "review_count": book["review_count"],
            "description": book["description"],
            "book_url": book["book_url"],
            "cover_image_url": book["cover_image_url"],
            # Price is optional in model but we have it
            "price": book.get("price") 
        }

        try:
            response = requests.post(api_url, json=payload)
            if response.status_code in [201, 200]:
                print(f"✅ Success: {book['title']}")
                success_count += 1
            else:
                print(f"❌ Failed: {book['title']} - {response.status_code} {response.text}")
                error_count += 1
        except Exception as e:
            print(f"❌ Error posting {book['title']}: {e}")
            error_count += 1

    print(f"\nFinished loading data.")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    load_to_db()
