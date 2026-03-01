from datetime import datetime, timezone

CATEGORY_CONFIG = {
    "Lab Blogs": {"emoji": "&#x1F9EA;", "label": "Lab Blogs"},
    "Tech News": {"emoji": "&#x1F4F0;", "label": "Tech News"},
    "AI Applications": {"emoji": "&#x1F680;", "label": "AI Applications"},
    "Research": {"emoji": "&#x1F4DA;", "label": "Research & Papers"},
    "Community": {"emoji": "&#x1F4AC;", "label": "Community Buzz"},
}

CATEGORY_ORDER = ["Lab Blogs", "Tech News", "AI Applications", "Research", "Community"]

# Source badge colors
SOURCE_COLORS = {
    "OpenAI": "#10a37f",
    "Google AI": "#4285f4",
    "Anthropic": "#d4a574",
    "DeepMind": "#5f6ff0",
    "Meta AI": "#0668e1",
    "Hugging Face": "#ffbd2e",
    "TechCrunch AI": "#00a562",
    "The Verge AI": "#e5127d",
    "Ars Technica": "#ff4e00",
    "MIT Tech Review": "#a51c30",
    "VentureBeat AI": "#93358a",
}

SECTION_COLORS = {
    "Lab Blogs": "#8b5cf6",
    "Tech News": "#0ea5e9",
    "AI Applications": "#f59e0b",
    "Research": "#10b981",
    "Community": "#6366f1",
}


def _article_html(article, is_top=False):
    source = article.get("source", "")
    title = article.get("title", "Untitled")
    url = article.get("url", "#")
    summary = article.get("summary", "")
    takeaway = article.get("takeaway", "")

    badge_bg = SOURCE_COLORS.get(source, "#64748b")
    border_color = "#6366f1" if is_top else "#e5e7eb"
    bg = "#fefce8" if is_top else "#ffffff"

    html = f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:12px;">
      <tr><td style="border-left:4px solid {border_color}; padding:14px 18px; background:{bg}; border-radius:6px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td>
            <a href="{url}" style="display:inline-block; background:{badge_bg}; color:#ffffff; font-size:10px; font-weight:600; padding:2px 8px; border-radius:3px; text-transform:uppercase; letter-spacing:0.5px; text-decoration:none;">{source}</a>
          </td>
        </tr></table>
        <a href="{url}" style="color:#111827; font-size:15px; font-weight:600; text-decoration:none; line-height:1.4; display:block; margin-top:8px;">{title}</a>"""

    if summary:
        html += f"""
        <p style="color:#6b7280; font-size:13px; line-height:1.5; margin:6px 0 0 0;">{summary}</p>"""

    if takeaway:
        html += f"""
        <p style="background:#f0f9ff; padding:8px 12px; margin:8px 0 0 0; font-size:12px; color:#1d4ed8; line-height:1.4; border-radius:4px;">
          <strong>Takeaway:</strong> {takeaway}
        </p>"""

    html += """
      </td></tr>
    </table>"""
    return html


def _section_html(category_key, articles):
    config = CATEGORY_CONFIG.get(category_key, {"emoji": "", "label": category_key})
    accent = SECTION_COLORS.get(category_key, "#6366f1")
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:32px;">
      <tr><td>
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td style="padding-bottom:12px; border-bottom:3px solid {accent};">
              <span style="font-size:20px; vertical-align:middle;">{config['emoji']}</span>
              <span style="color:#111827; font-size:17px; font-weight:700; vertical-align:middle; margin-left:6px;">{config['label']}</span>
              <span style="color:#9ca3af; font-size:12px; vertical-align:middle; margin-left:8px;">{len(articles)} article{'s' if len(articles) != 1 else ''}</span>
            </td>
          </tr>
        </table>
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px;">
          <tr><td>{''.join(_article_html(a) for a in articles)}</td></tr>
        </table>
      </td></tr>
    </table>"""


def render_email(summarized, raw_articles):
    today = datetime.now(timezone.utc).strftime("%B %d, %Y")
    total = sum(len(v) for v in raw_articles.values())

    body_sections = ""

    if summarized:
        top_urls = set(summarized.get("top_stories", []))
        categories = summarized.get("categories", {})

        # Collect top stories and remove them from categories
        top_articles = []
        for cat_key in list(categories.keys()):
            remaining = []
            for a in categories[cat_key]:
                if a.get("url") in top_urls:
                    top_articles.append(a)
                else:
                    remaining.append(a)
            categories[cat_key] = remaining

        if top_articles:
            body_sections += """
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:24px;">
              <tr><td>
                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                  <tr><td style="padding-bottom:12px; border-bottom:3px solid #f59e0b;">
                    <span style="font-size:20px; vertical-align:middle;">&#x2B50;</span>
                    <span style="color:#111827; font-size:17px; font-weight:700; vertical-align:middle; margin-left:6px;">Top Stories</span>
                  </td></tr>
                </table>
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px;">
                  <tr><td>"""
            body_sections += "".join(_article_html(a, is_top=True) for a in top_articles)
            body_sections += "</td></tr></table></td></tr></table>"

        for cat_key in CATEGORY_ORDER:
            articles = categories.get(cat_key, [])
            if articles:
                body_sections += _section_html(cat_key, articles)
    else:
        body_sections += """
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:16px;">
          <tr><td style="background:#fef3c7; padding:12px 16px; border-radius:6px; color:#92400e; font-size:14px;">
            AI summaries unavailable today — here are the raw links.
          </td></tr>
        </table>"""
        for cat_key in CATEGORY_ORDER:
            articles = raw_articles.get(cat_key, [])
            if articles:
                body_sections += _section_html(cat_key, articles)

    subject = f"AI News Digest — {today}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0; padding:0; background:#f3f4f6; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f3f4f6; padding:24px 0;">
<tr><td align="center">
<table width="620" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.08); overflow:hidden;">
  <tr><td style="background:#111827; padding:32px 36px;">
    <h1 style="color:#ffffff; font-size:26px; margin:0; font-weight:700; letter-spacing:-0.5px;">AI News Digest</h1>
    <p style="color:#9ca3af; font-size:13px; margin:8px 0 0 0;">{today} &middot; {total} articles curated from 16 sources</p>
  </td></tr>
  <tr><td style="padding:8px 36px 36px 36px;">
    {body_sections}
  </td></tr>
  <tr><td style="background:#f9fafb; padding:20px 36px; border-top:1px solid #e5e7eb;">
    <p style="color:#9ca3af; font-size:11px; margin:0; text-align:center;">
      Delivered by AI News Digest &middot; Curated from {total} articles across 16 sources
    </p>
  </td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""

    return subject, html
