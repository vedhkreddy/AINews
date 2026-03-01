import resend

from src.config import RESEND_API_KEY, SENDER_EMAIL, RECIPIENT_EMAIL

resend.api_key = RESEND_API_KEY


def send_email(subject, html_body, to_email=None):
    """Send the newsletter email via Resend.

    Returns the Resend response dict on success, raises on failure.
    """
    recipients = [e.strip() for e in (to_email or RECIPIENT_EMAIL).split(",") if e.strip()]
    params = {
        "from": f"AI News Digest <{SENDER_EMAIL}>",
        "to": recipients,
        "subject": subject,
        "html": html_body,
    }
    response = resend.Emails.send(params)
    print(f"Email sent to {len(recipients)} recipient(s)! ID: {response.get('id', 'unknown')}")
    return response
