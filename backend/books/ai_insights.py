import anthropic
from django.conf import settings

def get_claude_client():
    return anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

def generate_book_insights(description):
    """
    Calls Claude 3.5 Sonnet to generate summary, genre, and sentiment.
    """
    if not settings.ANTHROPIC_API_KEY:
        return {
            "summary": "AI summary unavailable (API key missing).",
            "genre": "Unknown",
            "sentiment": "Neutral"
        }

    client = get_claude_client()
    
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
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620", # Using 3.5 Sonnet as requested (or latest compatible)
            max_tokens=1000,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract response text
        response_text = message.content[0].text
        
        # Basic parsing (handling potential Claude prefix/suffix)
        import json
        import re
        
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
        print(f"Error calling Claude API: {e}")
        return {
            "summary": "Error generating AI summary.",
            "genre": "Unknown",
            "sentiment": "Neutral"
        }
