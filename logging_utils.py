import csv
import os
import uuid
import json

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
RESEARCH_DIRECTORY = os.path.join(LOG_DIRECTORY, "research")
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
    "Teacher Name",
    "Condition",
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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
    st.session_state.get("teacher_name", ""),
    st.session_state.get("condition", ""),
    timestamp,
    event_code
])

            file.flush()

    except Exception as e:

        print(
            f"[Logging Error] {e}"
        )

def save_research_session(
    inputs,
    lesson_plan,
    refined_lesson="",
    teacher_prior_knowledge="",
    teacher_misconceptions="",
    teacher_learning_difficulties="",
    conversation_history=None,
):
    """
    Saves one complete research session as a JSON file.
    """

    try:

        os.makedirs(
            RESEARCH_DIRECTORY,
            exist_ok=True
        )

        session_data = {

            "teacher_name":
                st.session_state.get(
                    "teacher_name",
                    ""
                ),

            "condition":
                st.session_state.get(
                    "condition",
                    ""
                ),

            "session_id":
                st.session_state.get(
                    "session_id",
                    ""
                ),

            "timestamp":
                get_timestamp(),

            "lesson_inputs":
                inputs,
            "ai_suggestions": {

                "prior_knowledge":
                    st.session_state.get(
                        "prior_knowledge_ai",
                        ""
                    ),

                "misconceptions":
                    st.session_state.get(
                        "misconceptions_ai",
                        ""
                    ),

                "learning_difficulties":
                    st.session_state.get(
                        "learning_difficulties_ai",
                        ""
                    ),
            },

            "teacher_additions": {

                "prior_knowledge":
                    teacher_prior_knowledge,

                "misconceptions":
                    teacher_misconceptions,

                "learning_difficulties":
                    teacher_learning_difficulties,
            },

            "clarification_questions":
                st.session_state.get(
                    "questions_list",
                    []
                ),

            "clarification_answers":
                st.session_state.get(
                    "answers",
                    []
                ),
            "conversation_history":
                conversation_history if conversation_history else [],

            "lesson_plan":
                lesson_plan,

            "initial_lesson":
                st.session_state.get(
        "initial_lesson",
        lesson_plan
    ),

            "final_lesson":
                refined_lesson if refined_lesson else lesson_plan,

            "refined_lesson":
                refined_lesson,

            "lesson_versions":
                st.session_state.get(
                    "lesson_versions",
                    []
                )
        }

        filename = os.path.join(
            RESEARCH_DIRECTORY,
            f"{session_data['session_id']}.json"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                session_data,
                f,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:

        print(
            f"[Research Logging Error] {e}"
        )