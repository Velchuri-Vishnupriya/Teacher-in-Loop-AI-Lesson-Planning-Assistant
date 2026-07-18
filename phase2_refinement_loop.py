import streamlit as st

from pdf_utils import generate_pdf
from gemini_utils import refine_lesson_with_ai

from lesson_parser_v2 import (
    parse_lesson_plan_v2,
)

from logging_utils import (
    log_event,
    save_research_session,
)

# =====================================================
# UI HELPERS
# =====================================================

def display_section_header(title):
    """
    Displays a clean section heading.
    """
    st.subheader(title)


def display_snapshot_card(snapshot):
    """
    Displays the Lesson Snapshot.
    """

    display_section_header("Lesson Snapshot")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Title**")
            st.markdown(snapshot["title"])

            st.markdown(f"**Subject**")
            st.markdown(snapshot["subject"])

            st.markdown(f"**Grade**")
            st.markdown(snapshot["grade"])

            st.markdown(f"**Board**")
            st.markdown(snapshot["board"])

        with col2:
            st.markdown(f"**Topic**")
            st.markdown(snapshot["topic"])

            st.markdown(f"**Duration**")
            st.markdown(snapshot["duration"])

            st.markdown(f"**Framework**")
            st.markdown(snapshot["framework"])




def display_text_card(title, text):
    """
    Displays a bordered text card.
    """

    display_section_header(title)

    with st.container(border=True):

        if text:
            st.write(text)
        else:
            st.caption("Not Available")


def display_content_card(title, content):
    """
    Displays a lesson section while preserving formatting.
    """

    display_section_header(title)

    with st.container(border=True):

        if not content or not content.strip():
            st.caption("Not Available")
            return

        st.markdown(
    content,
    unsafe_allow_html=False
)

import re

def display_lesson_flow_card(content):
    """
    Display each lesson stage in its own card.
    """

    display_section_header("Lesson Flow")

    if not content.strip():
        st.caption("Not Available")
        return

    # Split at stage numbers (1., 2., 3....)
    stages = re.split(r"\n(?=\d+\.\s)", content.strip())

    for stage in stages:

        stage = stage.strip()

        if not stage:
            continue

        with st.container(border=True):
            st.markdown(stage)

import re

def display_strategy_card(content):
    """
    Display every teaching strategy in a separate card.
    """

    display_section_header("Teaching Strategies")

    if not content.strip():
        st.caption("Not Available")
        return

    # Every strategy begins with a title followed by its explanation.
    blocks = re.split(r"\n\s*\n", content.strip())

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        with st.container(border=True):
            st.markdown(block)
# =====================================================
# PHASE 2
# =====================================================

def render_phase2():

    if not st.session_state.get("lesson_plan"):
        return

    lesson = parse_lesson_plan_v2(
        st.session_state.lesson_plan
    )
    if "refinement_chat_history" not in st.session_state:
        st.session_state.refinement_chat_history = []
    # ---------- DEBUG ----------
    #st.subheader("Raw Gemini Lesson")
    #st.text_area(
    #    "Raw Lesson Output",
    #    st.session_state.lesson_plan,
    #    height=600
    #)
    # ---------------------------
    st.divider()

    st.header(
        "Review, Refine and Finalize Lesson Plan"
    )

    st.info(
        "Review the generated lesson plan before editing or downloading."
    )

        # =====================================================
    # LESSON SNAPSHOT
    # =====================================================

    display_snapshot_card(
        lesson.get("snapshot", {})
    )

    st.divider()

    # =====================================================
    # LEARNING OBJECTIVES
    # =====================================================
    display_content_card(
    "Learning Objectives",
    lesson["learning_objectives"]
)

    st.divider()

    # =====================================================
    # LEARNER SNAPSHOT
    # =====================================================
    display_content_card(
        "Learner Snapshot",
        lesson["learner_snapshot"]
    )
    st.divider()
    # =====================================================
    # TEACHING STRATEGIES
    # =====================================================
    display_strategy_card(
        lesson["teaching_strategies"]
    )

    st.divider()

    # =====================================================
    # LESSON FLOW
    # =====================================================
    display_lesson_flow_card(
        lesson["lesson_flow"]
    )

    st.divider()

    # =====================================================
    # RESOURCES
    # =====================================================
    display_content_card(
    "Resources",
    lesson["resources"]
)

    st.divider()

    # =====================================================
    # ASSESSMENT
    # =====================================================
    display_content_card(
        "Assessment",
        lesson["assessment"]
    )
    st.divider()

    display_content_card(
    "Reflection",
    lesson["reflection"]
)
    st.divider()

    display_content_card(
        "Homework",
        lesson["homework"]
    )

    st.divider()

    display_content_card(
        "Teacher Notes",
        lesson["teacher_notes"]
    )

    st.divider()
    # =====================================================
    # AI REVIEW
    # =====================================================

    if st.session_state.get("lesson_review"):

        st.subheader("🤖 AI Review & Suggestions")

        st.info(
            "Review the AI suggestions before making further edits."
        )

        st.text_area(
            "Suggestions",
            value=st.session_state.lesson_review,
            height=250,
            disabled=True,
        )

    st.divider()
    # =====================================================
    # AI CONVERSATIONAL REFINEMENT
    # =====================================================

    st.subheader("🤖 AI Conversational Refinement")

    st.info(
        "Ask the AI to improve the generated lesson plan. "
        "Each request updates the lesson while preserving the previous conversation."
    )

    # -----------------------------
    # Display refinement history
    # -----------------------------

    for message in st.session_state.refinement_chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # -----------------------------
    # Teacher refinement request
    # -----------------------------

    teacher_request = st.chat_input(
        "Ask AI to improve this lesson..."
    )

    if teacher_request:

        st.session_state.refinement_chat_history.append(
            {
                "role": "user",
                "content": teacher_request,
            }
        )

        with st.spinner("Updating lesson..."):

            changes, updated_lesson = refine_lesson_with_ai(
    current_lesson=st.session_state.lesson_plan,
    teacher_request=teacher_request,
)

        st.session_state.lesson_plan = updated_lesson

        st.session_state.refinement_chat_history.append(
    {
        "role": "assistant",
        "content": changes
    }
)

        st.rerun()

    st.divider()

    # =====================================================
    # SAVE FINAL LESSON
    # =====================================================

    if st.button(
        "💾 Save Final Lesson",
        use_container_width=True,
    ):

        save_research_session(
            inputs=st.session_state.lesson_inputs,
            lesson_plan=st.session_state.lesson_plan,
            refined_lesson=st.session_state.lesson_plan,
            conversation_history=st.session_state.refinement_chat_history,
        )

        log_event("LESSON_REFINED")

    st.success("Final lesson saved successfully.")
    # =====================================================
    # DOWNLOAD PDF
    # =====================================================
    pdf = generate_pdf(
    st.session_state.lesson_plan
)

    download_clicked = st.download_button(
        label="📄 Download Lesson Plan PDF",
        data=pdf,
        file_name="lesson_plan.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    if download_clicked:
        log_event("PDF_EXPORTED")