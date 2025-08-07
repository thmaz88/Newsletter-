#!/usr/bin/env python3
"""Fetch daily food & beverage news using NewsAPI.

This script queries the NewsAPI service for recent articles related to
Food & Beverage and stores the results in a JSON file named with the
current date. Set the NEWS_API_KEY environment variable with your API key
before running.
"""

import datetime as _dt
import json
import os
import urllib.parse
import urllib.request

API_URL = "https://newsapi.org/v2/everything"
QUERY = "(alimentos OR bebidas OR \"food and beverage\")"
LANGUAGE = "pt"
MAX_RESULTS = 20


def fetch_news() -> dict:
    """Retrieve news articles from NewsAPI."""
    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        raise RuntimeError("NEWS_API_KEY environment variable not set")
    params = {
        "q": QUERY,
        "language": LANGUAGE,
        "sortBy": "publishedAt",
        "pageSize": MAX_RESULTS,
        "apiKey": api_key,
    }
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as resp:
        return json.load(resp)


def save_articles(data: dict) -> str:
    """Save the fetched articles to a JSON file named with today's date."""
    date_str = _dt.datetime.now().strftime("%Y-%m-%d")
    filename = f"news_{date_str}.json"
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    return filename


def main() -> None:
    data = fetch_news()
    filename = save_articles(data)
    print(f"Saved {len(data.get('articles', []))} articles to {filename}")


if __name__ == "__main__":
    main()
