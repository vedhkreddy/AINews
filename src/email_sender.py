import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL


def send_email(subject, html_body, to_email=None):
    """Send the newsletter email via Gmail SMTP.

    Returns None on success, raises on failure.
    """
    recipients = [e.strip() for e in (to_email or RECIPIENT_EMAIL).split(",") if e.strip()]

    msg = MIMEMultipart("alternative")
    msg["From"] = f"AI News Digest <{GMAIL_ADDRESS}>"
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, recipients, msg.as_string())

    print(f"Email sent to {len(recipients)} recipient(s)!")
