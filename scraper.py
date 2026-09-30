import os
from typing import Dict, List
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load key from .env
load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def fetch_google_serp(query: str, num: int = 10) -> List[Dict[str, str]]:
    #Sends a request to retrieve the first page of Google search results.
    
    if not SERPAPI_KEY:  
        raise ValueError("SERPAPI_KEY nebyl nalezen v .env souboru!")

    params = {
        "engine": "google",
        "q": query, 
        "location": "Czechia",
        "hl": "cs",
        "gl": "cz",
        "num": num, 
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    data = search.get_dict()

    if "error" in data:
        raise RuntimeError(f"Chyba SerpAPI: {data['error']}")

    return parse_serp_response(data)



def parse_serp_response(data: dict) -> List[Dict[str, str]]:
    #Pure function: accepts a raw JSON response and filters the data to include ONLY organic results (excluding paid advertisements).
    
    # SerpAPI already separates ads and organic_results
    organic_items = data.get("organic_results", [])
    results = []

    for item in organic_items:
        title = item.get("title", "").strip()
        url = item.get("link", "").strip()   
        snippet = item.get("snippet", "").strip()   
 
        # Empty elements 
        if not title or not url:
            continue

        results.append({
            "title": title,
            "url": url,   
            "snippet": snippet
        })

    return results