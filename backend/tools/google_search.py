"""
Google Search Tool
Provides web search capability for general queries
"""

import requests
import os


def google_search(query: str) -> str:
    """
    Perform a Google search (simplified version)
    
    Args:
        query: The search query
        
    Returns:
        Search results or a helpful message
    """
    # Note: This is a simplified implementation
    # For production, you'd want to use the official Google Search API
    # or a service like SerpAPI
    
    return f"""
    For general web searches about "{query}", I recommend:
    
    1. Check the official documentation for the most accurate information
    2. Visit Stack Overflow for technical questions
    3. Consult AWS/Azure/GCP official docs for cloud-specific queries
    
    💡 Tip: I'm best at helping with your team's internal documentation 
    and your live cloud infrastructure. For general questions, feel free 
    to use Google directly or ask me to search our internal docs!
    """


# Alternative: Use a real search API if you have credits
def google_search_api(query: str) -> str:
    """
    Real Google Search implementation using Custom Search API
    Requires: GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID
    """
    api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    
    if not api_key or not engine_id:
        return google_search(query)  # Fall back to simple version
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': engine_id,
            'q': query,
            'num': 3
        }
        
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if 'items' not in data:
            return "No search results found."
        
        results = []
        for item in data['items'][:3]:
            results.append(f"• {item['title']}\n  {item['snippet']}\n  {item['link']}\n")
        
        return "Top search results:\n\n" + "\n".join(results)
    
    except Exception as e:
        return f"Search error: {str(e)}"


# Test function
if __name__ == "__main__":
    result = google_search("kubernetes basics")
    print(result)
