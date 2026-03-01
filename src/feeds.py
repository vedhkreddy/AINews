import time
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

import feedparser

from src.config import FEEDS, LOOKBACK_HOURS


def _parse_published(entry):
    """Extract a UTC datetime from a feed entry, or None."""
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            return datetime(*t[:6], tzinfo=timezone.utc)
    return None


def _fetch_single_feed(source_name, url, cutoff):
    """Fetch one RSS feed and return articles newer than cutoff."""
    articles = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = _parse_published(entry)
            # Keep articles without a date (we can't filter them) and recent ones
            if published and published < cutoff:
                continue
            articles.append({
                "source": source_name,
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", "").strip(),
                "published": published.isoformat() if published else None,
                "summary": entry.get("summary", "")[:500].strip(),
            })
    except Exception as e:
        print(f"  [WARN] Failed to fetch {source_name}: {e}")
    return articles


def _deduplicate(articles):
    """Remove duplicates by normalized URL, keeping first occurrence."""
    seen_urls = set()
    seen_titles = set()
    unique = []
    for a in articles:
        url_key = a["url"].rstrip("/").lower()
        title_key = a["title"].lower()[:80]
        if url_key in seen_urls or title_key in seen_titles:
            continue
        seen_urls.add(url_key)
        seen_titles.add(title_key)
        unique.append(a)
    return unique


def fetch_articles():
    """Fetch all RSS feeds in parallel, filter to recent, deduplicate.

    Returns dict mapping category name to list of article dicts.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
    all_articles = {}

    for category, sources in FEEDS.items():
        category_articles = []
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = {
                pool.submit(_fetch_single_feed, name, url, cutoff): name
                for name, url in sources
            }
            for future in as_completed(futures):
                category_articles.extend(future.result())

        # Sort by published date descending (undated last)
        category_articles.sort(
            key=lambda a: a["published"] or "",
            reverse=True,
        )
        all_articles[category] = _deduplicate(category_articles)

    total = sum(len(v) for v in all_articles.values())
    print(f"Fetched {total} articles across {len(all_articles)} categories")
    return all_articles
