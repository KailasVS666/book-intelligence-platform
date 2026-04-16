import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_endpoint(name, url, method="GET", data=None):
    print(f"Testing {name}...", end=" ", flush=True)
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        if response.status_code in [200, 201]:
            print("PASSED")
            return response.json()
        else:
            print(f"FAILED (Status: {response.status_code})")
            print(f"Response: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"ERROR ({e})")

        return None

def run_suite():
    print("=== Document Intelligence Stability Test Suite ===\n")
    
    # 1. Test Book List
    books = test_endpoint("Book List", f"{BASE_URL}/books/")
    if not books or len(books) == 0:
        print("Stopping: No books found in DB.")
        return

    # 2. Test Single Book Detail
    test_id = books[0]['id']
    test_endpoint("Book Detail", f"{BASE_URL}/books/{test_id}/")

    # 3. Test Recommendations
    test_endpoint("Recommendations", f"{BASE_URL}/books/{test_id}/recommendations/")

    # 4. Test RAG Ask
    qa_data = {
        "question": "What is the main theme of this book?",
        "book_id": test_id
    }
    test_endpoint("RAG Ask", f"{BASE_URL}/books/ask/", method="POST", data=qa_data)

    print("\n=== Test Suite Complete ===")

if __name__ == "__main__":
    run_suite()
