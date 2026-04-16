import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_books(max_pages=5):
    """
    Scrapes book data from books.toscrape.com using Selenium.
    Returns a list of book dictionaries.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # In some environments, we might need to specify the path to chromedriver
    # For now, we rely on Selenium 4's automatic manager.
    driver = webdriver.Chrome(options=chrome_options)
    
    base_url = "http://books.toscrape.com/"
    books_data = []
    
    try:
        driver.get(base_url)
        current_page = 1
        
        while current_page <= max_pages:
            print(f"Scraping page {current_page}...")
            
            # Find all book items on the current page
            book_elements = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
            
            # Store links to follow to avoid stale element exceptions
            book_links = []
            for book in book_elements:
                link = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
                # Basic data from listing
                title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
                rating_class = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class")
                rating = rating_class.replace("star-rating ", "")
                price = book.find_element(By.CSS_SELECTOR, "p.price_color").text
                cover_image = book.find_element(By.CSS_SELECTOR, "img.thumbnail").get_attribute("src")
                
                book_links.append({
                    "url": link,
                    "title": title,
                    "rating": rating,
                    "price": price,
                    "cover_image_url": cover_image
                })
            
            # Visit each book's detail page
            for book_info in book_links:
                driver.get(book_info["url"])
                
                # Extract Description
                try:
                    # Description is usually the first paragraph after #product_description h2
                    # But it's simpler to use the sibling of the div with id product_description
                    description_header = driver.find_element(By.ID, "product_description")
                    description = description_header.find_element(By.XPATH, "./following-sibling::p").text
                except:
                    description = ""
                
                # Extract Review Count from table
                try:
                    table = driver.find_element(By.CSS_SELECTOR, "table.table-striped")
                    review_count_cell = table.find_element(By.XPATH, ".//th[text()='Number of reviews']/following-sibling::td")
                    review_count = int(review_count_cell.text)
                except:
                    review_count = 0
                
                # Extract Author (Note: books.toscrape.com doesn't actually have author names for most items)
                # We'll set it to "Unknown" or try to find it if it exists
                author = "Unknown"
                
                books_data.append({
                    "title": book_info["title"],
                    "author": author,
                    "rating": book_info["rating"],
                    "review_count": review_count,
                    "description": description,
                    "book_url": driver.current_url,
                    "cover_image_url": book_info["cover_image_url"],
                    "price": book_info["price"]
                })
                
                # Go back or return to previous page? Better to just go back or click the next page later.
                # Actually, driver.get(base_url) or next page is safer.
                
            # Move to next page
            try:
                driver.get(base_url) # Reset to home to find next button or relative link
                # This is tricky because base_url is the home. 
                # We need to ensure we are on the page were we found the book_links.
                # Let's adjust the logic to handle pagination better.
                pass 
            except:
                break
                
            # Re-navigating to the "current" collection page to find the next button
            # A better way is to track the URL of the listing page.
            break # Simplifying for now, let's fix the loop logic below.

    finally:
        driver.quit()
    
    return books_data

# Refined version of the loop logic for better pagination
def scrape_with_pagination(max_pages=3):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    url = "http://books.toscrape.com/catalogue/page-1.html"
    all_books = []
    
    try:
        for p in range(1, max_pages + 1):
            print(f"Scraping page {p}...")
            driver.get(url)
            
            book_elements = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
            current_page_links = []
            
            for book in book_elements:
                link = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
                title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
                rating_class = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class")
                rating_text = rating_class.replace("star-rating ", "")
                price = book.find_element(By.CSS_SELECTOR, "p.price_color").text
                cover_image = book.find_element(By.CSS_SELECTOR, "img.thumbnail").get_attribute("src")
                
                current_page_links.append({
                    "url": link,
                    "title": title,
                    "rating": rating_text,
                    "price": price,
                    "cover_image_url": cover_image
                })
                
            # Detail scraping
            for book_info in current_page_links:
                driver.get(book_info["url"])
                time.sleep(1) # Be polite
                
                try:
                    desc = driver.find_element(By.XPATH, "//div[@id='product_description']/following-sibling::p").text
                except:
                    desc = ""
                    
                try:
                    reviews = int(driver.find_element(By.XPATH, "//th[text()='Number of reviews']/following-sibling::td").text)
                except:
                    reviews = 0
                
                all_books.append({
                    "title": book_info["title"],
                    "author": "Unknown",
                    "rating_text": book_info["rating"],
                    "review_count": reviews,
                    "description": desc,
                    "book_url": driver.current_url,
                    "cover_image_url": book_info["cover_image_url"],
                    "price": book_info["price"]
                })
                print(f"  Scraped: {book_info['title']}")

            # Find next page URL
            try:
                driver.get(f"http://books.toscrape.com/catalogue/page-{p}.html") # Back to listing
                next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
                url = next_btn.get_attribute("href")
            except:
                print("No more pages found.")
                break
                
        # Save to file
        os.makedirs("scraper", exist_ok=True)
        with open("scraper/books_raw.json", "w", encoding="utf-8") as f:
            json.dump(all_books, f, indent=4, ensure_ascii=False)
        print(f"Successfully scraped {len(all_books)} books across {p} pages.")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_with_pagination(max_pages=2) # Default to 2 pages for testing
