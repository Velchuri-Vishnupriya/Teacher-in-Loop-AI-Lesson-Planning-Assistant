import streamlit as st

from phase4_export import (
    create_docx,
    create_pdf,
)
def render_phase3():

    if not st.session_state.get(
        "show_phase3",
        False,
    ):
        return

    st.divider()

    st.header(
        "Teacher Satisfaction & Rating"
    )

    satisfied = st.checkbox(
        "I am satisfied with the lesson plan."
    )

    if satisfied:

        st.session_state["satisfied"] = True

        rating = st.slider(
            "Rate the lesson plan",
            min_value=1,
            max_value=5,
            value=5,
        )

        st.session_state["rating"] = rating

        st.success(
            f"Rating Recorded: {rating}/5"
        )

        st.subheader(
            "Session Summary"
        )

        st.write(
            f"Total Refinement Rounds: "
            f"{st.session_state['refinement_round']}"
        )

        st.write(
            f"Teacher Rating: "
            f"{rating}/5"
        )

        st.success(
            "Teacher-in-the-Loop Session Completed!"
        )

        st.divider()

        st.subheader(
            "Download Lesson Plan"
        )

        docx_file = create_docx(
            st.session_state.lesson_plan
        )

        pdf_file = create_pdf(
            st.session_state.lesson_plan
        )

        st.download_button(
            label="Download DOCX",
            data=docx_file,
            file_name="lesson_plan.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name="lesson_plan.pdf",
            mime="application/pdf",
        )