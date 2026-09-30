import smtplib
import ssl
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

recipient = "ayonmukherjeegamer@gmail.com"
sender = "verify@masteryflow.edu"

msg = MIMEMultipart("alternative")
msg["Subject"] = "MasteryFlow Security OTP: 492817"
msg["From"] = "MasteryFlow AI Platform <verify@masteryflow.edu>"
msg["To"] = recipient
msg["Date"] = email.utils.formatdate(localtime=True)
msg["Message-ID"] = email.utils.make_msgid(domain="masteryflow.edu")

text_content = "Your MasteryFlow verification code is: 492817 (Valid for 10 minutes)."
html_content = """
<div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f6f8;">
  <div style="max-width: 500px; margin: auto; background: white; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0;">
    <h2 style="color: #1e3a8a; margin-top: 0;">MasteryFlow Verification</h2>
    <p style="color: #475569;">Your 6-digit verification code is:</p>
    <div style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #1e3a8a; background: #f1f5f9; padding: 14px; text-align: center; border-radius: 8px;">
      492817
    </div>
    <p style="color: #64748b; font-size: 12px; margin-top: 16px;">Valid for 10 minutes. If you did not request this, please ignore.</p>
  </div>
</div>
"""

msg.attach(MIMEText(text_content, "plain"))
msg.attach(MIMEText(html_content, "html"))

try:
    print("Connecting to gmail-smtp-in.l.google.com:25...")
    server = smtplib.SMTP("gmail-smtp-in.l.google.com", 25, timeout=15)
    server.set_debuglevel(1)
    server.ehlo("masteryflow.edu")
    
    context = ssl.create_default_context()
    server.starttls(context=context)
    server.ehlo("masteryflow.edu")
    
    server.mail(sender)
    server.rcpt(recipient)
    resp = server.data(msg.as_string())
    print("\n[RESULT]:", resp)
    server.quit()
except Exception as e:
    print("\n[ERROR]:", e)
