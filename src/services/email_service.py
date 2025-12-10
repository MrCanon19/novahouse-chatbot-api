import os


class EmailService:
    """
    A dummy email service for sending notifications.
    In a real application, this would integrate with an actual email provider.
    """

    def __init__(self):
        print("📧 EmailService initialized (dummy mode).")

    def send_email(self, to_email: str, subject: str, html_content: str):
        """
        Simulates sending an email.
        """
        print(f"\n--- DUMMY EMAIL SENT ---")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Content:\n{html_content}")
        print(f"------------------------\n")


# Global instance for compatibility, to be replaced by dependency injection
email_service = EmailService()
