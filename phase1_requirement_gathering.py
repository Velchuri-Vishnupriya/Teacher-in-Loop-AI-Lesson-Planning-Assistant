import streamlit as st

from gemini_utils import (
    generate_clarification_questions,
    generate_lesson_plan,
)


def render_phase1():

    # -----------------------------
    # Lesson Information
    # -----------------------------

    st.subheader("Lesson Information")

    grade_level = st.text_input("Grade Level")

    subject = st.text_input("Subject")

    topic = st.text_input("Topic")

    lesson_duration = st.text_input("Lesson Duration")

    # -----------------------------
    # Learning Objectives
    # -----------------------------

    st.subheader("Learning Objectives")

    learning_objective = st.text_area("Learning Objective / Key Concept")

    # -----------------------------
    # Learner Information
    # -----------------------------

    st.subheader("Learner Information")

    prior_knowledge = st.text_area("Prior Knowledge")

    misconceptions = st.text_area("Common Misconceptions")

    learning_difficulties = st.text_area("Learning Difficulties")

    # -----------------------------
    # Teacher Inputs
    # -----------------------------

    st.subheader("Teacher Inputs")

    activity_ideas = st.text_area("Teacher Activity Ideas")

    assessment_ideas = st.text_area("Teacher Assessment Ideas")

    # -----------------------------
    # Store Inputs
    # -----------------------------

    inputs = {
        "grade_level": grade_level,
        "subject": subject,
        "topic": topic,
        "lesson_duration": lesson_duration,
        "learning_objective": learning_objective,
        "prior_knowledge": prior_knowledge,
        "misconceptions": misconceptions,
        "learning_difficulties": learning_difficulties,
        "activity_ideas": activity_ideas,
        "assessment_ideas": assessment_ideas,
    }

    # -----------------------------
    # Generate Clarification Questions
    # -----------------------------

    if st.button("Generate Clarification Questions"):

        required_fields = [
            grade_level,
            subject,
            topic,
            learning_objective,
        ]

        if not all(field.strip() for field in required_fields):
            st.warning(
                "Please fill Grade Level, Subject, Topic, and Learning Objective."
            )
            st.stop()

        with st.spinner("Generating clarification questions..."):

            try:

                questions = generate_clarification_questions(**inputs)

                if not questions:
                    st.error(
                        "AI service is temporarily unavailable. Please try again."
                    )
                    st.stop()

                st.session_state.questions = questions

                st.session_state.questions_list = [
                    q.strip()
                    for q in questions.split("\n")
                    if q.strip()
                ]

            except Exception as e:
                st.error(f"Error: {e}")

    # -----------------------------
    # Display Questions
    # -----------------------------

    if st.session_state.get("questions_list", []):

        st.success("Clarification questions generated successfully!")

        st.subheader("AI Generated Clarification Questions")

        for i, question in enumerate(st.session_state.questions_list):

            st.write(question)

            st.text_area(
                f"Answer for Question {i+1}",
                key=f"answer_{i}"
            )

        # -------------------------
        # Save Responses
        # -------------------------

        if st.button("Save Clarification Responses"):

            answers = []

            for i in range(len(st.session_state.questions_list)):
                answers.append(
                    st.session_state.get(f"answer_{i}", "")
                )

            st.session_state.answers = answers

            st.success("Responses saved successfully!")

            st.subheader("Saved Responses")

            for i, answer in enumerate(st.session_state.answers):

                st.write(f"Answer {i+1}:")

                st.write(answer)

    # -----------------------------
    # Generate Lesson Plan
    # -----------------------------

    if st.session_state.get("answers", []):

        if st.button("Generate Lesson Plan"):

            with st.spinner("Generating lesson plan..."):

                try:

                    lesson_plan = generate_lesson_plan(
                        **inputs,
                        questions_list=st.session_state.questions_list,
                        answers=st.session_state.answers,
                    )

                    if not lesson_plan:
                        st.error(
                            "AI service is temporarily unavailable. Please try again."
                        )
                        st.stop()

                    st.session_state.lesson_plan = lesson_plan

                except Exception as e:
                    st.error(f"Error: {e}")

    # -----------------------------
    # Display Lesson Plan
    # -----------------------------

    if st.session_state.get("lesson_plan", ""):

        st.success("Lesson Plan Generated Successfully!")

        st.subheader("Generated Lesson Plan")

        st.markdown(st.session_state.lesson_plan)