import streamlit as st

def initialize_session_state():

    defaults = {
        "questions": "",
        "questions_list": [],
        "answers": [],
        "lesson_plan": "",

        "feedback_history": [],

        "refinement_questions": [],
        "refinement_answers": [],
        "refined_lesson_plan": "",
        "refinement_round": 0,
        "teacher_feedback": "",

        "satisfied": False,
        "rating": 0,

        # UI Control
        "show_refinement": False,
        "show_phase3": False,

        # Future Version Tracking
        "lesson_versions": [],
        "version_count": 0,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value