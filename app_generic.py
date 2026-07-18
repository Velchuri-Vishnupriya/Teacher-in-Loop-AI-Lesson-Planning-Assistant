import streamlit as st

from session_manager import initialize_session_state

from gemini_utils import chat_with_generic_llm
from logging_utils import (
    create_session_id,
    save_research_session,
    log_event,
)

from pdf_utils import generate_generic_pdf

st.set_page_config(
    page_title="Generic AI Lesson Planning Assistant",
    page_icon="💬",
    layout="wide",
)

initialize_session_state()

if "generic_chat_history" not in st.session_state:
    st.session_state.generic_chat_history = []

if "generic_teacher_name" not in st.session_state:
    st.session_state.generic_teacher_name = ""

if "generic_lesson" not in st.session_state:
    st.session_state.generic_lesson = ""

st.title("Generic AI Lesson Planning Assistant")

st.caption(
    "Conversational Lesson Planning using Gemini"
)
st.subheader("Teacher Information")

teacher_name = st.text_input(
    "Teacher Name",
    value=st.session_state.generic_teacher_name
)

st.session_state.generic_teacher_name = teacher_name
st.subheader("Lesson Information")

grade = st.text_input("Grade Level")

subject = st.text_input("Subject")

topic = st.text_input("Topic")

duration = st.text_input("Lesson Duration")

board = st.text_input("Board / Curriculum")
st.divider()

if st.button("Start Lesson Planning Session", use_container_width=True):

    if not all([teacher_name, grade, subject, topic, duration, board]):

        st.warning("Please fill all lesson information.")

    else:

        st.session_state.teacher_name = teacher_name
        st.session_state.condition = "Generic"
        log_event("SESSION_START")

        if not st.session_state.session_id:
            st.session_state.session_id = create_session_id()

        initial_prompt = f"""
I am planning a lesson.

Grade Level: {grade}

Subject: {subject}

Topic: {topic}

Lesson Duration: {duration}

Board/Curriculum: {board}

Let's start planning this lesson together.
"""

        st.session_state.generic_chat_history = [
            {
                "role": "user",
                "content": initial_prompt
            }
        ]

        response = chat_with_generic_llm(
            st.session_state.generic_chat_history
        )

        st.session_state.generic_chat_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()
st.divider()

st.subheader("Conversation")

for message in st.session_state.generic_chat_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Hide chat input once final lesson has been generated
if not st.session_state.get("lesson_plan"):

    user_message = st.chat_input(
        "Type your message..."
    )

    if user_message:

        st.session_state.generic_chat_history.append(
            {
                "role": "user",
                "content": user_message
            }
        )
        log_event("USER_MESSAGE")

        response = chat_with_generic_llm(
            st.session_state.generic_chat_history
        )

        st.session_state.generic_chat_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )
        log_event("AI_RESPONSE")

        st.rerun()

st.divider()

if st.button(
    "📋 Generate Final Lesson Plan",
    use_container_width=True,
):

    final_request = """
Based on our complete conversation above, prepare the final classroom-ready lesson plan.

Do not ask further clarification questions.

Return only the complete lesson plan.
"""

    conversation = st.session_state.generic_chat_history.copy()

    conversation.append(
        {
            "role": "user",
            "content": final_request
        }
    )

    final_lesson = chat_with_generic_llm(
        conversation
    )

    st.session_state.lesson_plan = final_lesson
    log_event("LESSON_GENERATED")

    save_research_session(
    inputs={
        "grade_level": grade,
        "subject": subject,
        "topic": topic,
        "lesson_duration": duration,
        "board": board,
    },
    lesson_plan=final_lesson,
    conversation_history=st.session_state.generic_chat_history,
)

    st.rerun()
if st.session_state.get("lesson_plan"):

    st.divider()

    st.subheader("📖 Final Lesson Plan (Preview)")

    st.info(
        "This is the formatted lesson plan. You can edit it below before saving or exporting."
    )

    formatted_lesson = (
    st.session_state.lesson_plan
    .replace("<br>", "\n")
    .replace("<br/>", "\n")
    .replace("<br />", "\n")
)
    st.markdown(formatted_lesson)

    st.divider()
# -------------------------------------------------------
# Save / Export
# -------------------------------------------------------
if st.button(
        "📄 Export as PDF",
        use_container_width=True,
    ):

        log_event("PDF_EXPORTED")
        pdf = generate_generic_pdf(
            st.session_state.lesson_plan
        )

        st.download_button(
            label="⬇ Download Lesson Plan PDF",
            data=pdf,
            file_name="generic_lesson_plan.pdf",
            mime="application/pdf",
            use_container_width=True,
        )