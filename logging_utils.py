import csv
import os
import uuid

from datetime import datetime

import streamlit as st


# =====================================================
# Configuration
# =====================================================

"""
Teacher Activity Logger

Current Backend:
CSV

Future Backend:
AWS RDS / CloudWatch

The rest of the application should always use:
    log_event(event_code)

Only this file needs to change if the logging
backend is upgraded in the future.
"""

LOG_DIRECTORY = "logs"
LOG_FILE = os.path.join(
    LOG_DIRECTORY,
    "teacher_activity_log.csv"
)


# =====================================================
# Session Management
# =====================================================

def create_session_id():
    """
    Generates a unique session ID
    for every teacher session.
    """
    return str(uuid.uuid4())[:8]


def get_timestamp():
    """
    Returns the current timestamp.
    """
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# =====================================================
# CSV Initialization
# =====================================================

def initialize_log_file():
    """
    Creates the log directory and CSV
    file if they do not exist.
    """

    os.makedirs(
        LOG_DIRECTORY,
        exist_ok=True
    )

    if not os.path.exists(LOG_FILE):

        with open(
            LOG_FILE,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Session ID",
                "Timestamp",
                "Event Code"
            ])

            file.flush()


# =====================================================
# Event Logger
# =====================================================

def log_event(event_code):
    """
    Appends a single event
    to the activity log.
    """

    try:

        initialize_log_file()

        session_id = st.session_state.get(
            "session_id",
            "UNKNOWN"
        )

        with open(
            LOG_FILE,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                session_id,
                get_timestamp(),
                event_code
            ])

            file.flush()

    except Exception as e:

        print(
            f"[Logging Error] {e}"
        )