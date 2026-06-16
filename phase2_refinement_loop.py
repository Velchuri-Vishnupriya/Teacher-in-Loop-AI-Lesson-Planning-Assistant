import streamlit as st

from gemini_utils import (
    generate_refinement_questions,
    generate_refined_lesson_plan,
)


def render_phase2():

    # Only show Phase 2 after lesson plan exists

    if not st.session_state.get("lesson_plan", ""):
        return

    st.divider()

    st.header("Next Step")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Refine Lesson Plan"
        ):

            st.session_state["show_refinement"] = True

            st.session_state["show_phase3"] = False

    with col2:

        if st.button(
            "Proceed to Satisfaction & Rating"
        ):

            st.session_state["show_phase3"] = True

            st.session_state["show_refinement"] = False

    # If teacher chooses satisfaction,
    # don't show refinement section

    if not st.session_state.get(
        "show_refinement",
        False,
    ):
        return

    st.divider()

    st.header(
        f"Refinement Round "
        f"{st.session_state['refinement_round'] + 1}"
    )

    # -------------------------
    # Teacher Feedback
    # -------------------------

    teacher_feedback = st.text_area(
        "What would you like to improve?",
        key=f"teacher_feedback_"
        f"{st.session_state['refinement_round']}"
    )

    # -------------------------
    # Generate Refinement Questions
    # -------------------------

    if st.button(
        "Generate Refinement Questions"
    ):

        if not teacher_feedback.strip():

            st.warning(
                "Please provide feedback first."
            )

        else:

            try:

                questions = (
                    generate_refinement_questions(
                        st.session_state.lesson_plan,
                        teacher_feedback,
                    )
                )

                st.session_state[
                    "teacher_feedback"
                ] = teacher_feedback

                st.session_state[
                    "refinement_questions"
                ] = [
                    q.strip()
                    for q in questions.split("\n")
                    if q.strip()
                ]

                st.session_state[
                    "refinement_answers"
                ] = []

            except Exception as e:

                st.error(f"Error: {e}")

    # -------------------------
    # Display Questions
    # -------------------------

    if st.session_state.get(
        "refinement_questions",
        [],
    ):

        st.subheader(
            "AI Refinement Questions"
        )

        for i, question in enumerate(
            st.session_state[
                "refinement_questions"
            ]
        ):

            st.write(question)

            st.text_area(
                f"Answer {i+1}",
                key=f"refinement_answer_{i}"
            )

        # -------------------------
        # Save Responses
        # -------------------------

        if st.button(
            "Save Refinement Responses"
        ):

            answers = []

            for i in range(
                len(
                    st.session_state[
                        "refinement_questions"
                    ]
                )
            ):

                answers.append(
                    st.session_state.get(
                        f"refinement_answer_{i}",
                        "",
                    )
                )

            st.session_state[
                "refinement_answers"
            ] = answers

            st.success(
                "Responses saved."
            )

    # -------------------------
    # Generate Refined Plan
    # -------------------------

    if st.session_state.get(
        "refinement_answers",
        [],
    ):

        if st.button(
            "Generate Refined Lesson Plan"
        ):

            try:

                refined_plan = (
                    generate_refined_lesson_plan(
                        st.session_state.lesson_plan,
                        st.session_state.teacher_feedback,
                        st.session_state.refinement_questions,
                        st.session_state.refinement_answers,
                    )
                )

                st.session_state[
                    "refined_lesson_plan"
                ] = refined_plan

                # New version becomes current

                st.session_state[
                    "lesson_plan"
                ] = refined_plan

                st.session_state[
                    "refinement_round"
                ] += 1

                st.session_state[
                    "refinement_questions"
                ] = []

                st.session_state[
                    "refinement_answers"
                ] = []

                # Hide refinement after completion

                st.session_state[
                    "show_refinement"
                ] = False

                st.success(
                    "Lesson Plan Refined Successfully!"
                )

            except Exception as e:

                st.error(f"Error: {e}")