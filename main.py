#!/usr/bin/env python3
"""AI News Newsletter — daily digest pipeline."""

import sys

from src.feeds import fetch_articles
from src.summarizer import summarize_articles
from src.template import render_email
from src.email_sender import send_email


def main():
    # 1. Fetch RSS feeds
    print("Fetching RSS feeds...")
    articles = fetch_articles()

    total = sum(len(v) for v in articles.values())
    if total == 0:
        print("No articles found. Skipping send.")
        return

    # 2. Summarize via Groq (falls back to None on failure)
    print("Summarizing with Groq...")
    summarized = summarize_articles(articles)
    if summarized:
        print("Summarization complete.")
    else:
        print("Summarization failed — sending raw article list as fallback.")

    # 3. Render HTML email
    print("Rendering email...")
    subject, html = render_email(summarized, articles)

    # Optional: save preview for local testing
    if "--preview" in sys.argv:
        with open("/tmp/ainews_preview.html", "w") as f:
            f.write(html)
        print("Preview saved to /tmp/ainews_preview.html")
        return

    # 4. Send via Resend
    print("Sending email...")
    send_email(subject, html)
    print("Done!")


if __name__ == "__main__":
    main()
