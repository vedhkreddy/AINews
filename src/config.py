import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
RESEND_API_KEY = os.environ["RESEND_API_KEY"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "onboarding@resend.dev")

GROQ_MODEL = "llama-3.3-70b-versatile"

# Hours to look back for articles
LOOKBACK_HOURS = 24

# RSS feeds grouped by category
FEEDS = {
    "Lab Blogs": [
        ("OpenAI", "https://openai.com/blog/rss.xml"),
        ("Google AI", "https://blog.google/technology/ai/rss/"),
        ("Anthropic", "https://www.anthropic.com/rss.xml"),
        ("DeepMind", "https://deepmind.google/blog/rss.xml"),
        ("Meta AI", "https://ai.meta.com/blog/rss/"),
        ("Hugging Face", "https://huggingface.co/blog/feed.xml"),
    ],
    "Tech News": [
        ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
        ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
        ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab"),
        ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
        ("The Decoder", "https://the-decoder.com/feed/"),
        ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ],
    "Research": [
        ("ArXiv cs.AI", "https://rss.arxiv.org/rss/cs.AI"),
        ("ArXiv cs.LG", "https://rss.arxiv.org/rss/cs.LG"),
    ],
    "Community": [
        ("Hacker News", "https://hnrss.org/newest?q=AI+OR+LLM+OR+GPT+OR+machine+learning&points=50"),
        ("Reddit r/ML", "https://www.reddit.com/r/MachineLearning/hot/.rss?limit=20"),
    ],
}
