import requests
from bs4 import BeautifulSoup

import os
import sys

# connect to Django backend
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from books.models import Book


def scrape_books():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    items = soup.select(".product_pod")

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    for item in items:
        title = item.h3.a["title"]
        price = item.select_one(".price_color").text

        rating_text = item.p["class"][1]
        rating = rating_map.get(rating_text, 0)

        books.append({
            "title": title,
            "price": price,
            "rating": rating
        })

    return books


if __name__ == "__main__":
    data = scrape_books()

    for book in data:
        # ✅ avoid duplicates
        if not Book.objects.filter(title=book["title"]).exists():
            Book.objects.create(
                title=book["title"],
                author="Unknown",
                rating=book["rating"],
                description="Scraped book from website",
                url=""
            )

    print("✅ Books successfully saved to database!")