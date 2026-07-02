import csv
import os
import uuid

from datetime import datetime

# =====================================================
# Configuration
# =====================================================

LOG_FILE = "teacher_activity_log.csv"

# =====================================================
# Session Management
# =====================================================

def create_session_id():
    """
    Generates a unique session ID for every teacher session.
    """
    return str(uuid.uuid4())[:8]


def get_timestamp():
    """
    Returns the current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =====================================================
# CSV Initialization
# =====================================================

def initialize_log_file():
    """
    Creates the log file with headers if it does not exist.
    """

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


# =====================================================
# Event Logger
# =====================================================

def log_event(event_code):
    import streamlit as st
    session_id = st.session_state.session_id
    """
    Appends a single event to the activity log.
    """

    initialize_log_file()

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