"""
MasteryFlow Email Service
Handles dispatching One-Time Password (OTP) verification emails via SMTP
with HTML formatting, fallback logging, and live credential management.
"""

import os
import smtplib
import ssl
import time
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Root directories for outbox logs and .env loading
BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / "data"
LOG_DIR.mkdir(parents=True, exist_ok=True)
OUTBOX_LOG_PATH = LOG_DIR / "email_outbox.log"

# In-memory history of recent dispatched emails
_OUTBOX_HISTORY: List[Dict[str, Any]] = []


def _load_env_file(force_reload: bool = False) -> None:
    """Loads key-value pairs from .env into os.environ."""
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        env_file = BASE_DIR.parent / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k:
                        if force_reload or not os.environ.get(k):
                            os.environ[k] = v
        except Exception:
            pass


# Automatically load .env on module import
_load_env_file()


def get_smtp_config() -> Dict[str, Any]:
    """
    Retrieves SMTP configuration from environment variables or Streamlit secrets.
    """
    _load_env_file()

    host = os.environ.get("SMTP_HOST") or os.environ.get("SMTP_SERVER") or "smtp.gmail.com"
    port_str = os.environ.get("SMTP_PORT", "587")
    try:
        port = int(port_str)
    except ValueError:
        port = 587

    username = os.environ.get("SMTP_USERNAME") or os.environ.get("SMTP_USER") or ""
    password = os.environ.get("SMTP_PASSWORD") or os.environ.get("SMTP_PASS") or ""
    from_email = os.environ.get("SMTP_FROM_EMAIL") or username or "no-reply@masteryflow.edu"
    from_name = os.environ.get("SMTP_FROM_NAME") or "MasteryFlow AI Platform"
    use_tls = os.environ.get("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")

    # Fallback to Streamlit secrets if running in Streamlit and env vars are empty
    if not username or not password:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "smtp" in st.secrets:
                s = st.secrets["smtp"]
                host = s.get("host", host)
                port = int(s.get("port", port))
                username = s.get("username", username)
                password = s.get("password", password)
                from_email = s.get("from_email", from_email)
                from_name = s.get("from_name", from_name)
        except Exception:
            pass

    return {
        "host": host,
        "port": port,
        "username": username.strip(),
        "password": password.strip(),
        "from_email": from_email.strip(),
        "from_name": from_name.strip(),
        "use_tls": use_tls,
    }


def is_smtp_configured() -> Tuple[bool, str]:
    """Checks whether valid SMTP credentials have been provided."""
    cfg = get_smtp_config()
    if not cfg["username"] or not cfg["password"]:
        return False, "SMTP credentials (username/password) not configured in .env."
    return True, f"Configured for {cfg['host']}:{cfg['port']} as {cfg['username']}"


def save_smtp_credentials(
    username: str,
    password: str,
    host: str = "smtp.gmail.com",
    port: int = 587,
    from_name: str = "MasteryFlow Platform"
) -> Tuple[bool, str]:
    """Saves SMTP credentials to .env file and active environment."""
    u = username.strip()
    p = password.strip().replace(" ", "")
    if not u or not p:
        return False, "Both Gmail address and 16-character App Password are required."
    
    os.environ["SMTP_HOST"] = host
    os.environ["SMTP_PORT"] = str(port)
    os.environ["SMTP_USERNAME"] = u
    os.environ["SMTP_PASSWORD"] = p
    os.environ["SMTP_FROM_EMAIL"] = u
    os.environ["SMTP_FROM_NAME"] = from_name
    os.environ["SMTP_USE_TLS"] = "true"

    env_content = f"""# MasteryFlow SMTP Email Configuration
SMTP_HOST={host}
SMTP_PORT={port}
SMTP_USERNAME={u}
SMTP_PASSWORD={p}
SMTP_FROM_EMAIL={u}
SMTP_FROM_NAME={from_name}
SMTP_USE_TLS=true
"""
    try:
        env_path = BASE_DIR / ".env"
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(env_content)
        
        # Also sync to sibling Hackathon - Copy directory if it exists
        copy_env = BASE_DIR.parent / "Hackathon - Copy" / ".env"
        if copy_env.parent.exists() and copy_env.parent.is_dir():
            try:
                with open(copy_env, "w", encoding="utf-8") as f:
                    f.write(env_content)
            except Exception:
                pass
                
        return True, "SMTP credentials saved and activated successfully."
    except Exception as exc:
        return False, f"Failed to save .env file: {exc}"


def test_smtp_connection(
    host: str = "smtp.gmail.com",
    port: int = 587,
    username: str = "",
    password: str = "",
    use_tls: bool = True
) -> Tuple[bool, str]:
    """Tests connecting and authenticating against the SMTP server."""
    u = username.strip()
    p = password.strip().replace(" ", "")
    if not u or not p:
        return False, "Username and password cannot be empty."
    try:
        if port == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, port, context=context, timeout=10) as server:
                server.login(u, p)
        else:
            with smtplib.SMTP(host, port, timeout=10) as server:
                server.ehlo()
                if use_tls:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                    server.ehlo()
                server.login(u, p)
        return True, f"Authentication succeeded for {u} via {host}:{port}!"
    except Exception as exc:
        return False, f"SMTP Error: {exc}"


def _build_otp_email_html(recipient_email: str, otp_code: str, user_name: Optional[str] = None) -> str:
    """Builds a responsive, modern HTML email body for OTP delivery."""
    greeting = f"Hello {user_name}," if user_name else "Hello Learner,"
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MasteryFlow Verification Code</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #F8FAFC; padding: 30px 15px;">
    <tr>
      <td align="center">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 540px; background-color: #FFFFFF; border-radius: 14px; border: 1px solid #E2E8F0; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
          <!-- Header -->
          <tr>
            <td style="background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%); padding: 28px 32px; text-align: left;">
              <div style="font-size: 22px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px;">
                MasteryFlow
              </div>
              <div style="font-size: 13px; color: #BFDBFE; margin-top: 4px; font-weight: 500;">
                Cognitive Diagnostic &amp; Adaptive Learning Engine
              </div>
            </td>
          </tr>
          <!-- Body Content -->
          <tr>
            <td style="padding: 32px 32px 24px 32px;">
              <p style="margin: 0 0 16px 0; font-size: 15px; color: #1E293B; line-height: 1.5; font-weight: 600;">
                {greeting}
              </p>
              <p style="margin: 0 0 20px 0; font-size: 14px; color: #475569; line-height: 1.6;">
                We received a request to verify your account for <strong>{recipient_email}</strong>. Use the One-Time Password (OTP) below to authenticate your session:
              </p>
              <!-- OTP Box -->
              <div style="background-color: #F1F5F9; border: 2px dashed #CBD5E1; border-radius: 12px; padding: 20px; text-align: center; margin: 24px 0;">
                <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 1.5px; margin-bottom: 6px;">
                  Your 6-Digit Verification Code
                </div>
                <div style="font-size: 34px; font-weight: 800; color: #1E3A8A; letter-spacing: 6px; font-family: 'Courier New', Courier, monospace;">
                  {otp_code}
                </div>
                <div style="font-size: 12px; color: #059669; font-weight: 600; margin-top: 6px;">
                  Valid for 10 minutes
                </div>
              </div>
              <p style="margin: 0 0 12px 0; font-size: 13px; color: #64748B; line-height: 1.5;">
                If you did not initiate this request, you can safely ignore this email. Your account credentials remain secure.
              </p>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="background-color: #F8FAFC; border-top: 1px solid #E2E8F0; padding: 18px 32px; text-align: center;">
              <p style="margin: 0; font-size: 11px; color: #94A3B8; line-height: 1.4;">
                This is an automated security dispatch from the MasteryFlow Educational Engine.<br>
                Please do not reply directly to this email.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def _log_to_outbox_file(recipient_email: str, otp_code: str, status: str, details: str = "") -> None:
    """Appends dispatch log to data/email_outbox.log and in-memory list."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "recipient": recipient_email,
        "otp": otp_code,
        "status": status,
        "details": details,
    }
    _OUTBOX_HISTORY.insert(0, entry)
    if len(_OUTBOX_HISTORY) > 50:
        _OUTBOX_HISTORY.pop()

    try:
        with open(OUTBOX_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Recipient: {recipient_email} | OTP: {otp_code} | Status: {status} | Details: {details}\n")
    except Exception:
        pass


def send_otp_email(
    recipient_email: str,
    otp_code: str,
    user_name: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Sends an OTP verification email to the user.
    
    1. If SMTP credentials are configured, sends via smtplib.
    2. If SMTP is not configured or transmission fails, logs safely to outbox file
       and memory without raising exceptions.
    
    Returns:
        (success: bool, status_message: str)
    """
    recipient_clean = recipient_email.strip()
    if not recipient_clean:
        return False, "Recipient email is empty."

    cfg = get_smtp_config()
    is_configured, reason = is_smtp_configured()

    # If SMTP credentials are not configured, simulate delivery safely
    if not is_configured:
        _log_to_outbox_file(recipient_clean, otp_code, "SIMULATED_LOCAL", "SMTP credentials not configured in .env")
        return False, "SMTP credentials not configured in .env"

    # Prepare MIME Email Message with RFC 5322 compliance
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your MasteryFlow Verification Code: {otp_code}"
    msg["From"] = f"{cfg['from_name']} <{cfg['from_email']}>"
    msg["To"] = recipient_clean
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = email.utils.make_msgid(domain="masteryflow.edu")

    text_body = (
        f"MasteryFlow Verification Code\n\n"
        f"Your 6-digit OTP code is: {otp_code}\n\n"
        f"This code will expire in 10 minutes. If you did not request this, please ignore this message.\n"
    )
    html_body = _build_otp_email_html(recipient_clean, otp_code, user_name)

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    # Connect to SMTP server and transmit
    try:
        host = cfg["host"]
        port = cfg["port"]
        use_tls = cfg["use_tls"]

        if port == 465:
            # SSL port
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, port, context=context, timeout=12) as server:
                server.login(cfg["username"], cfg["password"])
                server.send_message(msg)
        else:
            # Standard STARTTLS port (e.g. 587)
            with smtplib.SMTP(host, port, timeout=12) as server:
                server.ehlo()
                if use_tls:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                    server.ehlo()
                server.login(cfg["username"], cfg["password"])
                server.send_message(msg)

        _log_to_outbox_file(recipient_clean, otp_code, "DELIVERED_SMTP", f"Sent via {host}:{port}")
        return True, f"Verification email successfully sent to {recipient_clean}."

    except Exception as exc:
        err_msg = str(exc)
        _log_to_outbox_file(recipient_clean, otp_code, "SMTP_ERROR", err_msg)
        return False, f"SMTP transmission error: {err_msg}"


def get_outbox_history(limit: int = 10) -> List[Dict[str, Any]]:
    """Returns the most recent dispatched emails."""
    return _OUTBOX_HISTORY[:limit]
