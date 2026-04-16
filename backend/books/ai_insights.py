from typing import Dict, Any
import ollama
from django.conf import settings
import json
import re

def generate_book_insights(description: str) -> Dict[str, Any]:
    """
    Analyzes book description using a local LLM to extract structured metadata.
    Returns: Dict containing 'summary', 'genre', and 'sentiment'.
    """
    model_name = getattr(settings, "OLLAMA_MODEL", "deepseek-r1:latest")
    
    prompt = f"""
    Analyze the following book description and provide a professional assessment in JSON format.
    Fields required:
    1. "summary": A concise 3-5 sentence summary.
    2. "genre": The most relevant genre (e.g., Fiction, Tech, History).
    3. "sentiment": One of [Positive, Neutral, Negative, Mixed].

    Response must be valid JSON only.

    Description:
    {description}
    """
    
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1}
        )
        
        content = response['message']['content']
        
        # Robust JSON extraction from LLM response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return {
                "summary": data.get("summary", ""),
                "genre": data.get("genre", "Unknown"),
                "sentiment": data.get("sentiment", "Neutral")
            }
            
    except Exception as e:
        # Fallback for inference failures
        pass

    return {
        "summary": description[:500] + "...",
        "genre": "General",
        "sentiment": "Neutral"
    }

