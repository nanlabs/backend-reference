from email.message import EmailMessage
from smtplib import SMTP, SMTPException
from typing import Any, Self

from app.config import settings


class EmailServiceException(Exception):
    pass


class EmailService:
    def __init__(self, smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    @classmethod
    def initialize(cls) -> Self | None:
        if not (
            settings.email.smtp_host
            and settings.email.smtp_port
            and settings.email.smtp_user
            and settings.email.smtp_password
            and settings.email.from_email
            and settings.email.to_email
        ):
            return None
        return cls(
            smtp_host=settings.email.smtp_host,
            smtp_port=settings.email.smtp_port,
            smtp_user=settings.email.smtp_user,
            smtp_password=settings.email.smtp_password,
        )

    def send_email(  # pylint: disable=too-many-arguments
        self,
        from_email: str,
        to_email: str,
        subject: str,
        body: str,
        attachments: list[dict[str, Any]] | None = None,
    ) -> None:
        message = EmailMessage()
        message["From"] = from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)
        if attachments:
            for attachment in attachments:
                message.add_attachment(
                    attachment["content"],
                    maintype=attachment["maintype"],
                    subtype=attachment["subtype"],
                    filename=attachment["filename"],
                )
        try:
            with SMTP(self.smtp_host, self.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.smtp_user, self.smtp_password)
                smtp.send_message(message)
        except SMTPException as e:
            raise EmailServiceException(f"Error sending email: {e}") from e
