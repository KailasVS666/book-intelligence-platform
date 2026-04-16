import ollama
from django.conf import settings
import json
import re

def generate_book_insights(description):
    """
    Calls local Ollama (Llama 3) to generate summary, genre, and sentiment.
    """
    model_name = getattr(settings, "OLLAMA_MODEL", "llama3")
    
    prompt = f"""
    Analyze the following book description and provide three things:
    1. A 3-5 sentence summary of the book.
    2. The most likely genre (e.g., Fiction, Sci-Fi, Mystery, Romance, etc.).
    3. The overall sentiment (Positive, Negative, Neutral, or Mixed).

    Format the response strictly as JSON with keys: "summary", "genre", "sentiment".
    
    Book Description:
    {description}
    """

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0
            }
        )
        
        response_text = response['message']['content']
        
        # Basic parsing (handling potential model prefix/suffix)
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            insights = json.loads(json_match.group())
            return insights
        else:
            return {
                "summary": response_text[:500],
                "genre": "Unknown",
                "sentiment": "Neutral"
            }
            
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return {
            "summary": "Error generating AI summary. Ensure Ollama is running (`ollama run llama3`).",
            "genre": "Unknown",
            "sentiment": "Neutral"
        }
