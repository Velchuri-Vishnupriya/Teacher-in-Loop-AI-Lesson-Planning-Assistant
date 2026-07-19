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

st.subheader("Start the Session")

st.info(
    "Click 'Start Conversation' to begin planning your lesson with the AI. "
    "Continue the conversation until you are satisfied, then click "
    "'Generate Final Lesson Plan'."
)

# -------------------------------
# Display chat history
# -------------------------------

for message in st.session_state.generic_chat_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -------------------------------
# Start Conversation
# -------------------------------

if len(st.session_state.generic_chat_history) == 0:

    if st.button(
        "💬 Start Conversation",
        use_container_width=True,
    ):

        if not all([teacher_name, grade, subject, topic, duration, board]):

            st.warning("Please fill all lesson information.")

            st.stop()

        st.session_state.teacher_name = teacher_name
        st.session_state.condition = "Generic"

        if not st.session_state.session_id:

            st.session_state.session_id = create_session_id()

        log_event("SESSION_START")

        opening_prompt =f"""
System Prompt (Background Only)

You are an experienced instructional designer and physics teacher helping a colleague plan a classroom lesson.

Respond helpfully and conversationally.

Ask clarifying questions if you need more information.

When asked, provide complete, practical lesson plans suitable for classroom use.

--------------------------------------------------

The teacher has already provided the following lesson information:

Grade Level: {grade}

Subject: {subject}

Topic: {topic}

Lesson Duration: {duration}

Board/Curriculum: {board}

--------------------------------------------------

This is the beginning of the conversation.

Do NOT generate the complete lesson plan yet.

Instead:

• Greet the teacher naturally.
• Acknowledge the lesson information provided.
• Briefly describe your understanding of the lesson topic.
• Ask a few relevant questions to understand the teacher's preferences for designing the lesson (for example, teaching approach, classroom activities, assessment, or student engagement).
• Keep the interaction conversational, similar to ChatGPT or Gemini.

This is the first assistant response in the conversation.
"""

        response = chat_with_generic_llm(
            [
                {
                    "role": "user",
                    "content": opening_prompt
                }
            ]
        )

        st.session_state.generic_chat_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        log_event("AI_RESPONSE")

        st.rerun()

# -------------------------------
# Continue Conversation
# -------------------------------

elif not st.session_state.get("lesson_plan"):

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
if (
    len(st.session_state.generic_chat_history) > 0
    and st.button(
        "📋 Generate Final Lesson Plan",
        use_container_width=True,
    )
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

# -------------------------------------------------------
# Save / Export
# -------------------------------------------------------
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