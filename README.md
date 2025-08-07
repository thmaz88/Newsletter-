# Newsletter

Ferramenta simples para montar uma newsletter diária sobre **Alimentos e Bebidas**.

## Como funciona

- `news_fetcher.py` busca automaticamente notícias em uma fonte RSS e salva as
  10 mais recentes em `data/news.json`.
- `news_writer.py` lê o arquivo salvo e gera um boletim em texto localizado em
  `output/newsletter.txt`, com a manchete e a fonte oficial de cada notícia.

Execute `python news_fetcher.py` periodicamente (por exemplo, via cron) ao
longo do dia e, ao final, rode `python news_writer.py` para obter a newsletter.
"""Fetches news about food and beverages and stores them as JSON.

This module acts as the first agent. It downloads the latest news from an
RSS feed and keeps only a limited number of entries. Results are saved in
``data/news.json``.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

import feedparser

FEED_URL = (
    "https://news.google.com/rss/search?q=Alimentos+e+Bebidas&hl=pt-BR&gl=BR&ceid=BR:pt-419"
)


def fetch_news(limit: int = 10) -> List[Dict[str, str]]:
    """Fetches ``limit`` news items from ``FEED_URL``.

    Parameters
    ----------
    limit:
        Maximum number of news items to return.
    Returns
    -------
    List[Dict[str, str]]
        A list containing the news items with title, link, source and
        publication date when available.
    """
    feed = feedparser.parse(FEED_URL)
    items: List[Dict[str, str]] = []

    for entry in feed.entries[:limit]:
        items.append(
            {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "source": entry.get("source", {}).get("title", ""),
                "published": entry.get("published", ""),
            }
        )

    return items


def store_news(items: List[Dict[str, str]], path: str = "data/news.json") -> None:
    """Stores news ``items`` into ``path``.

    The directory for ``path`` is created automatically when necessary.
    """
    json_path = Path(path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    news = fetch_news()
    store_news(news)
    print(f"Stored {len(news)} items in data/news.json")
"""Reads stored news and produces a text newsletter.

This module acts as the second agent. It loads data produced by
``news_fetcher`` and writes a simple text file with the headline and the
original source of each news item.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict


def load_news(path: str = "data/news.json") -> List[Dict[str, str]]:
    """Loads news items from ``path`` and returns them."""
    json_path = Path(path)
    if not json_path.exists():
        raise FileNotFoundError(
            "No news data found. Run news_fetcher.py before running this script."
        )
    with json_path.open(encoding="utf-8") as f:
        return json.load(f)


def write_newsletter(items: List[Dict[str, str]], path: str = "output/newsletter.txt") -> None:
    """Writes ``items`` into a human readable newsletter at ``path``."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    for idx, item in enumerate(items, start=1):
        source = item.get("source") or "Fonte desconhecida"
        lines.append(f"{idx}. {item.get('title', '')} (Fonte: {source})")

    output_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    news_items = load_news()
    write_newsletter(news_items)
    print("Newsletter escrita em output/newsletter.txt")
feedparser>=6.0.10
