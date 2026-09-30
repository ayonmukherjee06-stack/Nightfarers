"""MasteryFlow Unified Authentication Component (login.py).

Provides a proper, production-grade Sign In & Registration interface
featuring email and password inputs, role-based authentication (Student & Educator),
form validation, SQLite credential persistence,
and 1-click quick demo fills for hackathon evaluators.
Designed according to the Apitex Porcelain & Obsidian design system.
"""

from __future__ import annotations
import hashlib
import re
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import streamlit as st
from frontend.components.theme import apply_theme, render_html, clean_html

import sys
BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from backend.api.db import (
        register_user,
        register_new_user,
        authenticate_user,
        find_user_by_email,
        reset_user_password,
        init_auth_db,
        hash_password as _hash_password,
        generate_user_otp,
        verify_user_otp,
        update_user_name,
        DB_PATH,
    )
    from backend.api.email_service import (
        send_otp_email,
        get_smtp_config,
        is_smtp_configured,
        get_outbox_history,
        save_smtp_credentials,
        test_smtp_connection,
    )
except ImportError:
    from masteryflow.api.db import (
        register_user,
        register_new_user,
        authenticate_user,
        find_user_by_email,
        reset_user_password,
        init_auth_db,
        hash_password as _hash_password,
        generate_user_otp,
        verify_user_otp,
        update_user_name,
        DB_PATH,
    )
    from masteryflow.api.email_service import (
        send_otp_email,
        get_smtp_config,
        is_smtp_configured,
        get_outbox_history,
        save_smtp_credentials,
        test_smtp_connection,
    )


def _login_session(user: Dict[str, Any], custom_name: Optional[str] = None) -> None:
    """Sets session state variables and redirects to the authenticated workspace."""
    role = user.get("role", "student")
    user_id = user.get("profile_id") or user.get("user_id") or user.get("student_id", "STU_042")
    final_name = custom_name.strip() if custom_name and custom_name.strip() else user.get("name", "Learner")

    # Strict Requirement 4: State Management
    st.session_state["authenticated"] = True
    st.session_state["user_id"] = user_id
    st.session_state["user_role"] = role

    if role == "teacher":
        st.session_state["teacher_id"] = user_id
        st.session_state["teacher_name"] = final_name
        st.session_state["portal_navigation"] = "Teacher Desk"
    else:
        st.session_state["student_id"] = user_id
        st.session_state["student_name"] = final_name
        st.session_state["virtual_days"] = 21.0 if user_id == "STU_004" else 0.0
        st.session_state["latest_attempt_result"] = None
        st.session_state["portal_navigation"] = "Learn"

    # Clear prefill keys
    st.session_state.pop("_auth_prefill_name", None)
    st.session_state.pop("_auth_prefill_email", None)
    st.session_state.pop("_auth_prefill_pw", None)
    st.session_state.pop("_auth_prefill_otp", None)

    # Strict Requirement 5: Rerun Logic
    st.rerun()


def render_combined_login_page() -> None:
    """Renders the comprehensive Sign In and Register portal."""
    apply_theme()
    init_auth_db()

    # Center column layout with proportional golden ratio (approx 480px width)
    _, col_center, _ = st.columns([1.15, 1.35, 1.15])

    with col_center:
        # Luxury Apitex Scoped Styling for Login Card
        render_html("""
        <style>
        [data-testid="stForm"] {
            background: #FFFFFF !important;
            border: 1px solid rgba(228, 221, 211, 0.95) !important;
            border-radius: 22px !important;
            padding: 26px 28px 22px 28px !important;
            box-shadow: 0 12px 36px -4px rgba(60, 50, 30, 0.06), 0 2px 8px -1px rgba(60, 50, 30, 0.02) !important;
            margin-bottom: 16px !important;
        }
        [data-testid="stForm"] button[kind="primaryFormSubmit"] {
            border-radius: 9999px !important;
            font-weight: 700 !important;
            padding-top: 10px !important;
            padding-bottom: 10px !important;
            letter-spacing: -0.01em !important;
            background: #11141D !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 6px 20px -2px rgba(17, 20, 29, 0.25) !important;
            transition: all 0.18s ease !important;
        }
        [data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
            background: #242938 !important;
            box-shadow: 0 8px 24px -2px rgba(17, 20, 29, 0.35) !important;
            transform: translateY(-1px) !important;
        }
        .demo-card-box {
            background: #FFFFFF;
            border: 1px solid rgba(228, 221, 211, 0.9);
            border-radius: 18px;
            padding: 16px 18px;
            margin-top: 14px;
            box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.03);
        }
        </style>
        """)

        # Apitex Platform Brand Header
        render_html("""
        <div style="text-align: center; margin-top: 6px; margin-bottom: 20px;">
            <div style="
                width: 46px;
                height: 46px;
                border-radius: 14px;
                background: #11141D;
                color: #FFFFFF;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 1.30rem;
                font-weight: 900;
                box-shadow: 0 8px 24px -4px rgba(17, 20, 29, 0.25);
                margin-bottom: 10px;
            ">▲</div>
            <h1 style="color: #11141D; margin: 0; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.03em;">
                Mastery<span style="color: #78716C; font-weight: 600;">Flow</span>
            </h1>
            <p style="color: #78716C; font-size: 0.84rem; margin-top: 4px;">
                Adaptive Cognitive Platform &middot; Apitex Luxury Edition
            </p>
        </div>
        """)

        # Main Authentication Tabs: Sign In vs Create Account
        tab_signin, tab_register = st.tabs([
            "Sign In",
            "Create Account",
        ])

        # =====================================================================
        # 1. SIGN IN TAB
        # =====================================================================
        with tab_signin:
            render_html("""
            <div style="margin-bottom: 14px;">
                <div style="font-size: 1.02rem; font-weight: 800; color: #11141D;">
                    Welcome back
                </div>
                <div style="font-size: 0.80rem; color: #78716C; margin-top: 2px;">
                    Enter your Email and Password to access your dashboard.
                </div>
            </div>
            """)

            # Prefilled credentials if selected via quick pills
            prefill_name = st.session_state.get("_auth_prefill_name", "")
            prefill_email = st.session_state.get("_auth_prefill_email", "")
            prefill_pw = st.session_state.get("_auth_prefill_pw", "")

            with st.form("signin_form", clear_on_submit=False):
                # Role toggle for Sign In
                login_role = st.radio(
                    "Sign In Role:",
                    options=["Student Portal", "Educator Desk"],
                    index=0 if st.session_state.get("_prefill_role") != "teacher" else 1,
                    horizontal=True,
                    label_visibility="collapsed",
                    key="signin_role_radio"
                )

                # Form input fields: Name, Email, Password
                name_input = st.text_input(
                    "Name",
                    value=prefill_name,
                    placeholder="e.g. Ayon Mukherjee",
                    key="auth_field_name"
                )

                email_input = st.text_input(
                    "Email",
                    value=prefill_email,
                    placeholder="e.g. ayonmukherjeegamer@gmail.com",
                    key="auth_field_email"
                )

                pw_input = st.text_input(
                    "Password",
                    value=prefill_pw,
                    type="password",
                    placeholder="Enter your password",
                    key="auth_field_password"
                )

                c_rem, c_forgot = st.columns([1, 1])
                with c_rem:
                    st.checkbox("Remember me", value=True, key="chk_remember_me")
                with c_forgot:
                    st.markdown(
                        "<div style='text-align: right; padding-top: 3px;'><span style='color: #78716C; font-size: 0.78rem; cursor: pointer;'>Forgot password?</span></div>",
                        unsafe_allow_html=True
                    )

                # Primary Sign In Button
                signin_submitted = st.form_submit_button("Sign In to MasteryFlow →", type="primary", use_container_width=True)

                # Handle Sign In Submission
                if signin_submitted:
                    clean_email = email_input.strip()
                    clean_pw = pw_input.strip()
                    clean_name = name_input.strip()

                    if not clean_email:
                        st.error("Please enter your email address.")
                    elif not clean_pw:
                        st.error("Please enter your password.")
                    else:
                        success, msg, user_data = authenticate_user(
                            clean_email,
                            clean_pw,
                            name=clean_name if clean_name else None
                        )
                        if success and user_data:
                            final_name = clean_name if clean_name else user_data["name"]
                            st.success(f"Welcome back, {final_name}! Access granted.")
                            time.sleep(0.3)
                            _login_session(user_data, custom_name=final_name)
                        else:
                            st.error(msg)

            with st.expander("Forgot your password? Reset here", expanded=False):
                with st.form("reset_password_form", clear_on_submit=False):
                    rp_email = st.text_input("Account Email Address", placeholder="name@masteryflow.edu", key="rp_email")
                    rp_new_pw = st.text_input("New Password (min 6 characters)", type="password", key="rp_new_pw")
                    rp_btn = st.form_submit_button("Reset Password", use_container_width=True)
                    if rp_btn:
                        ok, r_msg = reset_user_password(rp_email, rp_new_pw)
                        if ok:
                            st.success(r_msg)
                        else:
                            st.error(r_msg)

            # Quick 1-Click Demo Logins for Hackathon Evaluators
            render_html("""
            <div style="margin-top: 18px; margin-bottom: 8px;">
                <div style="font-size: 0.72rem; font-weight: 800; color: #78716C; text-transform: uppercase; letter-spacing: 0.5px;">
                    1-Click Demo Profiles (Instant Sign In)
                </div>
            </div>
            """)

            # Prominent 1-click pill for registered student Ayon Mukherjee
            if st.button("Ayon Mukherjee (Registered Student · STU_365)", use_container_width=True, key="pill_ayon"):
                st.session_state["_auth_prefill_name"] = "Ayon Mukherjee"
                st.session_state["_auth_prefill_email"] = "ayonmukherjeegamer@gmail.com"
                st.session_state["_auth_prefill_pw"] = "Ayon@2005"
                st.session_state["_auth_prefill_otp"] = ""
                st.session_state["_prefill_role"] = "student"
                _, _, u = authenticate_user("ayonmukherjeegamer@gmail.com", "Ayon@2005", name="Ayon Mukherjee")
                if u:
                    _login_session(u, custom_name="Ayon Mukherjee")

            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("Diya (Prereq Gap)", use_container_width=True, key="pill_diya"):
                    st.session_state["_auth_prefill_name"] = "Diya Sharma"
                    st.session_state["_auth_prefill_email"] = "diya@masteryflow.edu"
                    st.session_state["_auth_prefill_pw"] = "student123"
                    st.session_state["_auth_prefill_otp"] = ""
                    st.session_state["_prefill_role"] = "student"
                    _, _, u = authenticate_user("diya@masteryflow.edu", "student123", name="Diya Sharma")
                    if u:
                        _login_session(u, custom_name="Diya Sharma")

                if st.button("Aarav (Stuck Plateau)", use_container_width=True, key="pill_aarav"):
                    st.session_state["_auth_prefill_name"] = "Aarav Patel"
                    st.session_state["_auth_prefill_email"] = "aarav@masteryflow.edu"
                    st.session_state["_auth_prefill_pw"] = "student123"
                    st.session_state["_auth_prefill_otp"] = ""
                    st.session_state["_prefill_role"] = "student"
                    _, _, u = authenticate_user("aarav@masteryflow.edu", "student123", name="Aarav Patel")
                    if u:
                        _login_session(u, custom_name="Aarav Patel")

            with col_d2:
                if st.button("Priya (Top Performer)", use_container_width=True, key="pill_priya"):
                    st.session_state["_auth_prefill_name"] = "Priya Singh"
                    st.session_state["_auth_prefill_email"] = "priya@masteryflow.edu"
                    st.session_state["_auth_prefill_pw"] = "student123"
                    st.session_state["_auth_prefill_otp"] = ""
                    st.session_state["_prefill_role"] = "student"
                    _, _, u = authenticate_user("priya@masteryflow.edu", "student123", name="Priya Singh")
                    if u:
                        _login_session(u, custom_name="Priya Singh")

                if st.button("Dr. Shukla (Educator)", use_container_width=True, key="pill_shukla"):
                    st.session_state["_auth_prefill_name"] = "Dr. S. Shukla"
                    st.session_state["_auth_prefill_email"] = "shukla@masteryflow.edu"
                    st.session_state["_auth_prefill_pw"] = "teacher123"
                    st.session_state["_auth_prefill_otp"] = ""
                    st.session_state["_prefill_role"] = "teacher"
                    _, _, u = authenticate_user("shukla@masteryflow.edu", "teacher123", name="Dr. S. Shukla")
                    if u:
                        _login_session(u, custom_name="Dr. S. Shukla")

        # =====================================================================
        # 2. CREATE ACCOUNT (REGISTER) TAB
        # =====================================================================
        with tab_register:
            render_html("""
            <div style="margin-bottom: 14px;">
                <div style="font-size: 1.02rem; font-weight: 800; color: #11141D;">
                    Create your Account
                </div>
                <div style="font-size: 0.80rem; color: #78716C; margin-top: 2px;">
                    Register with your email to start your personalized adaptive learning journey.
                </div>
            </div>
            """)

            with st.form("register_form", clear_on_submit=False):
                reg_role = st.radio(
                    "Registering As:",
                    options=["Student Account", "Educator Account"],
                    index=0,
                    horizontal=True,
                    key="reg_role_radio"
                )
                is_student = "Student" in reg_role

                reg_name = st.text_input(
                    "Full Name",
                    placeholder="e.g. Maya Sharma" if is_student else "e.g. Prof. R. Verma",
                    key="reg_input_name"
                )

                reg_email = st.text_input(
                    "Email Address",
                    placeholder="e.g. maya@school.edu" if is_student else "e.g. verma@academy.edu",
                    key="reg_input_email"
                )

                if is_student:
                    reg_detail = st.selectbox(
                        "Enrolled Curriculum / Grade Level:",
                        options=[
                            "Grade 6 Mathematics (Standard)",
                            "Grade 6 Mathematics (Advanced Honors)",
                            "Grade 5 Foundational Review",
                            "Grade 7 Early Progression",
                        ],
                        key="reg_input_grade"
                    )
                else:
                    reg_detail = st.text_input(
                        "Department / School Affiliation:",
                        value="Department of Mathematics & Cognitive Diagnostics",
                        key="reg_input_dept"
                    )

                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    reg_pw = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Min 6 characters",
                        key="reg_input_pw"
                    )
                with col_p2:
                    reg_pw_conf = st.text_input(
                        "Confirm Password",
                        type="password",
                        placeholder="Repeat password",
                        key="reg_input_pw_conf"
                    )

                reg_agreed = st.checkbox(
                    "I agree to the MasteryFlow Terms of Service and Honor Code",
                    value=True,
                    key="reg_chk_terms"
                )

                # Primary Register Form Submit Button
                register_submitted = st.form_submit_button("Create Account & Launch Platform →", type="primary", use_container_width=True)

                # Handle Register Account Creation
                if register_submitted:
                    clean_reg_email = reg_email.strip()

                    if not reg_agreed:
                        st.warning("Please agree to the Terms of Service to create an account.")
                    elif not clean_reg_email or "@" not in clean_reg_email:
                        st.error("Please enter a valid email address.")
                    elif not reg_pw:
                        st.error("Please enter a password.")
                    elif reg_pw != reg_pw_conf:
                        st.error("Passwords do not match. Please ensure both password fields match.")
                    else:
                        role_key = "student" if is_student else "teacher"
                        success, msg, new_user = register_new_user(
                            name=reg_name,
                            email=reg_email,
                            password=reg_pw,
                            role=role_key,
                            dept_or_grade=reg_detail,
                        )
                        if success and new_user:
                            st.success(msg)
                            time.sleep(0.5)
                            _login_session(new_user, custom_name=reg_name.strip())
                        else:
                            st.error(msg)

        # Clean Security Footer
        render_html("""
        <div style="text-align: center; margin-top: 24px; padding-top: 14px; border-top: 1px solid rgba(228, 221, 211, 0.7); font-size: 0.74rem; color: #A8A29E;">
            Protected by MasteryFlow Engine &middot; SQLite Encrypted Auth &middot; BKT &middot; Prerequisite Topology
        </div>
        """)
