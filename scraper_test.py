import pytest
from scraper import parse_serp_response

# Test data simulating a raw search result response
MOCK_API_RESPONSE = {
    "ads": [
        {
            "position": 1,
            "title": "Placená reklama na SEO",
            "link": "https://adwords.google.com"
        }
    ],
    
    "organic_results": [
        {
            "position": 1,
            "title": "Collabim - SEO nástroj pro profesionály",
            "link": "https://www.collabim.cz/",
            "snippet": "Nejznámější český SEO nástroj pro měření pozic a analýzu klíčových slov."
        },
        {
            "position": 2,
            "title": "Inizio Internet Media",
            "link": "https://www.inizio.cz/",
            "snippet": "Internetový marketing, vývoj webových aplikací a SEO správa."
        },
        
        {
            "position": 3,
            "title": "Prázdný výsledek",
            "link": "",
            "snippet": ""
        }
    ]
}

def test_parse_serp_response_extracts_only_valid_organics():
    #Testing

    results = parse_serp_response(MOCK_API_RESPONSE)

    #There must be exactly 2 valid elements (excluding ads and any empty third element).
    assert len(results) == 2

    # Checking the frst element (Collabim)
    assert results[0]["title"] == "Collabim - SEO nástroj pro profesionály"
    assert results[0]["url"] == "https://www.collabim.cz/"
    assert "Nejznámější český SEO nástroj" in results[0]["snippet"]

    # Checking the secnd element (Inizio)
    assert results[1]["title"] == "Inizio Internet Media"
    assert results[1]["url"] == "https://www.inizio.cz/"

def test_parse_serp_response_handles_empty_data():
    #Check if the search returned an empty result.

    results = parse_serp_response({})
    assert results == []