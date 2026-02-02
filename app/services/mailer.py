from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings


async def send_email(
    to_email: str,
    subject: str,
    message_html: str,
    message_text: str | None = None
):
    """
    Асинхронная отправка email через SMTP.
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = "noreply@damon-dev.ru"
    msg["To"] = to_email
    msg["Subject"] = subject

    # Текстовая версия
    if message_text:
        msg.attach(MIMEText(message_text, "plain", "utf-8"))

    # HTML версия
    msg.attach(MIMEText(message_html, "html", "utf-8"))

    smtp = SMTP(
        hostname="smtp.beget.com",
        port=465,
        use_tls=True,              # implicit SSL
        username="noreply@damon-dev.ru",
        password="Qwert5432!"
    )

    try:
        await smtp.connect()
        await smtp.sendmail(
            "noreply@damon-dev.ru",
            [to_email],
            msg.as_string()
        )
        await smtp.quit()
        print("OK — письмо отправлено")
        return True


    except Exception as e:
        print(f"[Mailer] Ошибка отправки письма: {e}")
        return False


            # hostname=settings.SMTP_HOST,
            # port=settings.SMTP_PORT,
            # username=settings.SMTP_USER,
            # password=settings.SMTP_PASSWORD,
            # use_tls=settings.SMTP_TLS,
