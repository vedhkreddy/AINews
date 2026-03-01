import json

from groq import Groq

from src.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are an AI news editor writing a concise daily digest.

You will receive articles grouped by category. Your jobs:

1. INCLUDE ALL ARTICLES: Keep every article you receive. Do NOT drop any articles.
2. DEDUPLICATE ONLY if two articles are about the EXACT same event/announcement. When deduplicating, keep the one with the most detail.
3. CATEGORIZE: Place each article in exactly one category. Articles about real-world AI usage in specific industries (healthcare, finance, legal, creative, manufacturing, education, etc.) go in "AI Applications".
4. SUMMARIZE: Be concise — 1-2 sentences max per article.

For each article produce:
- "title": original title
- "url": original URL
- "source": source name
- "summary": 1-2 sentences, concise
- "takeaway": 1 sentence — the "so what" (why it matters, what it means)

Pick the top 3 most important stories and return their URLs in "top_stories". These stories should NOT appear again in any category section.

Categories to use: "Lab Blogs", "Tech News", "AI Applications", "Research", "Community"

Respond with ONLY valid JSON:
{
  "top_stories": ["url1", "url2", "url3"],
  "categories": {
    "Category Name": [
      {"title": "...", "url": "...", "source": "...", "summary": "...", "takeaway": "..."}
    ]
  }
}"""


def _build_user_prompt(articles_by_category):
    """Format articles into a prompt for the LLM."""
    lines = []
    for category, articles in articles_by_category.items():
        if not articles:
            continue
        lines.append(f"\n## {category}\n")
        for a in articles[:15]:  # Cap per category to stay within token limits
            lines.append(f"- **{a['title']}** ({a['source']})")
            lines.append(f"  URL: {a['url']}")
            if a["summary"]:
                lines.append(f"  Excerpt: {a['summary'][:200]}")
    return "\n".join(lines)


def summarize_articles(articles_by_category):
    """Send articles to Groq for summarization. Returns structured dict.

    On failure, returns None (caller should use fallback).
    """
    user_prompt = _build_user_prompt(articles_by_category)
    if not user_prompt.strip():
        return None

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=6000,
            response_format={"type": "json_object"},
        )
        text = response.choices[0].message.content
        return json.loads(text)
    except Exception as e:
        print(f"  [WARN] Groq summarization failed: {e}")
        return None
