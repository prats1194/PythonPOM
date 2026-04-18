"""
Email Pytest Report Utility
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email_conf import *


class EmailPytestReport:
    """Send pytest HTML reports via email"""

    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
        self.to_email = TO_EMAIL

    def get_report_data(self, report_file_path):
        """Read HTML report file"""
        if not os.path.exists(report_file_path):
            raise Exception(f"Report file '{report_file_path}' does not exist")

        with open(report_file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def create_attachment(self, report_file_path):
        """Create email attachment from report file"""
        with open(report_file_path, 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())

        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            'attachment',
            filename=os.path.basename(report_file_path)
        )
        return attachment

    def send_report(self, report_file_path, subject="Playwright Test Report"):
        """Send test report via email"""
        # Create message
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = ', '.join(self.to_email)
        message['Subject'] = subject

        # Email body
        body = """
        Hello,

        Please find the attached Playwright test report.

        Regards,
        Automation Team
        """
        message.attach(MIMEText(body, 'plain'))

        # Attach report
        try:
            attachment = self.create_attachment(report_file_path)
            message.attach(attachment)
        except Exception as e:
            print(f"❌ Failed to create attachment: {e}")
            return False

        # Send email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(
                    self.sender_email,
                    self.to_email,
                    message.as_string()
                )
            print(f"✅ Report sent successfully to {self.to_email}")
            return True  # ← SUCCESS: Return True

        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
            print("💡 Tip: Make sure you're using an App Password, not your regular password")
            return False  # ← FAILURE: Return False

        except smtplib.SMTPException as e:
            print(f"❌ SMTP error: {e}")
            return False  # ← FAILURE: Return False

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False  # ← FAILURE: Return False