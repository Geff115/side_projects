#!/usr/bin/env python3
"""
Generating morning updates using REST APIs.

API Keys used is:
    - NewsAPI API Key
    - MeteorSource API Key
    - Openai API Key
"""

import os
import requests


def get_morning_updates():
    """Getting news update from newsapi API"""
    # Fetching newsapi api key from the environment variable
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY:
        return "ERROR: NEWS_API_KEY environment variable not set"

    # setting a dict for the url parameter for newsapi
    news_api_url_parameter = {
        'apiKey': NEWS_API_KEY,
        'country': 'us'
    }
    # Sending request to the top-headlines endpoint
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params=news_api_url_parameter
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"

    # Evaluating the response
    response_data = response.json()

    # List comp to get the headline articles
    headline_articles = [
        {
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "publishedAt": article.get("publishedAt") 
        }
        for article in response_data.get("articles", [])
        if article.get("title") and article.get("title") != "Removed" and "Removed" not in article.get("title")
    ]
    return {"morning_updates": headline_articles}
