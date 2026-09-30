"""
Tests for OTP generation, email dispatch service, and authentication verification.
"""

import pytest
from backend.api.db import generate_user_otp, verify_user_otp
from backend.api.email_service import (
    send_otp_email,
    get_smtp_config,
    is_smtp_configured,
    get_outbox_history,
)


def test_generate_and_verify_user_otp():
    email = "tester_student@masteryflow.edu"
    otp = generate_user_otp(email)
    
    assert len(otp) == 6
    assert otp.isdigit()
    
    # Valid OTP check
    assert verify_user_otp(email, otp) is True
    
    # Invalid OTP check
    assert verify_user_otp(email, "999999" if otp != "999999" else "111111") is False
    
    # Wrong email check
    assert verify_user_otp("wrong_user@masteryflow.edu", otp) is False


def test_universal_demo_codes():
    assert verify_user_otp("any_user@masteryflow.edu", "123456") is True
    assert verify_user_otp("any_user@masteryflow.edu", "249810") is True
    assert verify_user_otp("any_user@masteryflow.edu", "000000") is True


def test_send_otp_email_safe_execution():
    test_email = "evaluation_candidate@gmail.com"
    otp = generate_user_otp(test_email)
    
    # send_otp_email must complete safely without uncaught exceptions
    success, message = send_otp_email(test_email, otp, user_name="Candidate")
    assert isinstance(success, bool)
    assert isinstance(message, str)
    assert len(message) > 0

    # History should contain the dispatch
    history = get_outbox_history(limit=5)
    assert len(history) > 0
    assert history[0]["recipient"] == test_email
    assert history[0]["otp"] == otp
