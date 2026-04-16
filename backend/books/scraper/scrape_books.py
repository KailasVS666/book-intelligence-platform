import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin

def scrape_with_pagination(max_pages=2):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    
    base_url = "http://books.toscrape.com/"
    start_url = "http://books.toscrape.com/catalogue/page-1.html"
    all_books = []
    
    try:
        current_listing_url = start_url
        for p in range(1, max_pages + 1):
            print(f"Scraping page {p}...")
            driver.get(current_listing_url)
            
            book_elements = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
            current_page_links = []
            
            for book in book_elements:
                try:
                    link = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
                    title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
                    rating_class = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class")
                    rating_text = rating_class.replace("star-rating ", "")
                    price = book.find_element(By.CSS_SELECTOR, "p.price_color").text
                    # Listing thumbnail as fallback
                    thumb_img = book.find_element(By.CSS_SELECTOR, "img.thumbnail").get_attribute("src")
                    
                    current_page_links.append({
                        "url": link,
                        "title": title,
                        "rating": rating_text,
                        "price": price,
                        "cover_image_url": thumb_img
                    })
                except Exception as e:
                    print(f"  Error extracting listing info: {e}")

            # NOW: Visit detail pages (OUTSIDE the book_elements loop)
            for book_info in current_page_links:
                try:
                    driver.get(book_info["url"])
                    time.sleep(0.3)
                    
                    try:
                        desc_el = driver.find_element(By.ID, "product_description")
                        desc = desc_el.find_element(By.XPATH, "./following-sibling::p").text
                    except:
                        desc = ""
                        
                    try:
                        reviews = int(driver.find_element(By.XPATH, "//th[text()='Number of reviews']/following-sibling::td").text)
                    except:
                        reviews = 0

                    try:
                        # Higher res image from detail page
                        main_img = driver.find_element(By.CSS_SELECTOR, ".item.active img")
                        high_res_url = main_img.get_attribute("src")
                        # Handle relative URLs
                        high_res_url = urljoin(driver.current_url, high_res_url)
                    except:
                        high_res_url = book_info["cover_image_url"]
                    
                    all_books.append({
                        "title": book_info["title"],
                        "author": "Unknown",
                        "rating_text": book_info["rating"],
                        "review_count": reviews,
                        "description": desc,
                        "book_url": driver.current_url,
                        "cover_image_url": high_res_url,
                        "price": book_info["price"]
                    })
                    print(f"  Scraped: {book_info['title']}")
                except Exception as e:
                    print(f"  Error scraping detail for {book_info['title']}: {e}")

            # Find next page URL
            try:
                driver.get(current_listing_url) # Back to listing to find next button
                next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
                current_listing_url = next_btn.get_attribute("href")
            except:
                print("No more pages found.")
                break
                
        # Save to file (in correct location)
        save_dir = os.path.join(os.path.dirname(__file__))
        save_path = os.path.join(save_dir, "books_raw.json")
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(all_books, f, indent=4, ensure_ascii=False)
        print(f"Successfully scraped {len(all_books)} books across {p} pages.")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_with_pagination(max_pages=2)
