import streamlit as st

from gemini_utils import (
    generate_ai_suggestions,
    generate_clarification_questions,
    generate_lesson_plan,
    review_lesson_plan,
)

from logging_utils import (
    create_session_id,
    log_event,
    save_research_session,
)

def render_phase1():
    if not st.session_state.session_id:
        st.session_state.session_id = create_session_id()

    if "questions_list" not in st.session_state:
        st.session_state.questions_list = []

    if "answers" not in st.session_state:
        st.session_state.answers = []

    if "lesson_plan" not in st.session_state:
        st.session_state.lesson_plan = ""

    if "lesson_review" not in st.session_state:
        st.session_state.lesson_review = ""

    st.subheader("Teacher Information")

    teacher_name = st.text_input(
        "Teacher Name"
    )

    st.session_state.teacher_name = teacher_name
    st.session_state.condition = "Scaffolded"

    if (
    teacher_name.strip()
    and not st.session_state.session_started
):
        log_event("SESSION_START")
        st.session_state.session_started = True
    # =====================================================
    # LESSON INFORMATION
    # =====================================================

    st.subheader("Lesson Information")

    grade_level = st.text_input(
        "Grade Level"
    )

    subject = st.text_input(
        "Subject"
    )

    topic = st.text_input(
        "Topic"
    )

    lesson_duration = st.text_input(
        "Lesson Duration"
    )
    board = "CBSE"
    st.text_input(
    "Board / Curriculum",
    value="CBSE",
    disabled=True,
)
    framework = "5E Model"
    st.text_input(
    "Instructional Framework",
    value="5E Learning Cycle",
    disabled=True,
)

    # =====================================================
    # LEARNING OBJECTIVES
    # =====================================================

    st.subheader("Learning Objectives")

    learning_objective = st.text_area(
        "Learning Objective / Key Concept"
    )
    # =====================================================
    # LEARNER INFORMATION
    # =====================================================

    st.subheader("Learner Information")

    # -----------------------------------------------------
    # Generate AI Learner Profile
    # -----------------------------------------------------

    if st.button(
        "Generate AI Learner Profile",
        use_container_width=True,
    ):

        if not topic.strip():

            st.warning(
                "Please enter the lesson topic first."
            )

        else:

            with st.spinner(
                "Generating learner profile..."
            ):

                try:

                    learner_profile = generate_ai_suggestions(
                        suggestion_type="Learner Profile",
                        grade_level=grade_level,
                        subject=subject,
                        topic=topic,
                        board=board,
                    )

                    st.session_state.learner_profile = learner_profile
                    st.session_state.show_profile = True
                    save_research_session(
    inputs=st.session_state.lesson_inputs,
    lesson_plan=st.session_state.get("lesson_plan", ""),
)
                    

                except Exception as e:

                    st.error(e)

    # -----------------------------------------------------
    # AI Suggestions Popup
    # -----------------------------------------------------

    if st.session_state.get("show_profile", False):

        @st.dialog("AI Suggested Learner Profile")
        def learner_profile_dialog():

            st.markdown(
                st.session_state.learner_profile
            )

            if st.button(
                "Close",
                use_container_width=True,
            ):

                st.session_state.show_profile = False
                st.rerun()

        learner_profile_dialog()

    # -----------------------------------------------------
    # Teacher Additions
    # -----------------------------------------------------

    st.markdown("### Additional Prior Knowledge")

    prior_knowledge = st.text_area(
        "Additional Prior Knowledge (Optional)",
        height=120,
    )

    st.markdown("### Additional Misconceptions")

    misconceptions = st.text_area(
        "Additional Misconceptions (Optional)",
        height=120,
    )

    st.markdown("### Additional Learning Difficulties")

    learning_difficulties = st.text_area(
        "Additional Learning Difficulties (Optional)",
        height=120,
    )           
    # =====================================================
    # STORE INPUTS
    # =====================================================

    inputs = {

        "grade_level": grade_level,

        "subject": subject,

        "topic": topic,

        "lesson_duration": lesson_duration,

        "board": board,

        "framework": framework,

        "learning_objective": learning_objective,

        "prior_knowledge": prior_knowledge,

        "misconceptions": misconceptions,

        "learning_difficulties": learning_difficulties,
    }
    st.session_state.lesson_inputs = inputs
    if (
    prior_knowledge.strip()
    and not st.session_state.prior_logged
):
        log_event("PRIOR_KNOWLEDGE_PROVIDED")
        st.session_state.prior_logged = True

    if (
    misconceptions.strip()
    and not st.session_state.misconceptions_logged
):
        log_event("MISCONCEPTIONS_PROVIDED")
        st.session_state.misconceptions_logged = True

    if (
    learning_difficulties.strip()
    and not st.session_state.learning_difficulties_logged
):
        log_event("LEARNING_DIFFICULTIES_PROVIDED")
        st.session_state.learning_difficulties_logged = True

    save_research_session(
    inputs=st.session_state.lesson_inputs,
    lesson_plan=st.session_state.get("lesson_plan", ""),
    teacher_prior_knowledge=prior_knowledge,
    teacher_misconceptions=misconceptions,
    teacher_learning_difficulties=learning_difficulties,
)

    # =====================================================
    # OPTIONAL AI CLARIFICATION QUESTIONS
    # =====================================================

    st.subheader("Clarification Questions")

    clarification_required = st.radio(
        "Would you like AI clarification questions before generating the lesson plan?",
        (
            "No",
            "Yes",
        ),
        horizontal=True,
    )
        # -----------------------------------------------------
    # YES → GENERATE QUESTIONS
    # -----------------------------------------------------

    if clarification_required == "Yes":

        if st.button(
            "Generate Clarification Questions"
        ):

            required_fields = [
                grade_level,
                teacher_name,
                subject,
                topic,
                learning_objective,
            ]

            if not all(
                field.strip()
                for field in required_fields
            ):

                st.warning(
                    "Please fill Grade Level, Subject, Topic and Learning Objective."
                )

                st.stop()

            with st.spinner(
                "Generating clarification questions..."
            ):

                try:

                    questions = generate_clarification_questions(
                        **inputs
                    )

                    if not questions:

                        st.error(
                            "Unable to generate clarification questions."
                        )

                        st.stop()

                    st.session_state.questions_list = [

                        q.strip()

                        for q in questions.split("\n")

                        if q.strip()

                    ]
                    
                    log_event("CLARIFICATION_QUESTIONS_GENERATED")

                except Exception as e:

                    st.error(f"Error: {e}")

        # ---------------------------------------------
        # DISPLAY QUESTIONS
        # ---------------------------------------------

        if st.session_state.get(
            "questions_list",
            [],
        ):

            st.success(
                "Clarification questions generated."
            )

            st.subheader(
                "AI Generated Clarification Questions"
            )

            for i, question in enumerate(
                st.session_state.questions_list
            ):

                st.write(question)

                st.text_area(
                    f"Answer {i + 1}",
                    key=f"answer_{i}",
                )

            if st.button(
                "Save Clarification Responses"
            ):

                answers = []

                for i in range(
                    len(
                        st.session_state.questions_list
                    )
                ):

                    answers.append(

                        st.session_state.get(
                            f"answer_{i}",
                            "",
                        )

                    )

                st.session_state.answers = answers

                log_event("CLARIFICATION_SUBMITTED")

                st.success(
                    "Responses saved successfully."
                )

    # -----------------------------------------------------
    # NO → CLEAR OLD QUESTIONS
    # -----------------------------------------------------

    else:

        st.session_state.questions_list = []
        st.session_state.answers = []

    # =====================================================
    # GENERATE LESSON PLAN
    # =====================================================

    can_generate = False

    questions_list = []
    answers = []

    if clarification_required == "No":

        can_generate = True

    else:

        if st.session_state.get(
            "answers",
            [],
        ):

            can_generate = True

            questions_list = st.session_state.get(
                "questions_list",
                [],
            )

            answers = st.session_state.get(
                "answers",
                [],
            )

    if st.button(
        "Generate Lesson Plan"
    ):

        required_fields = [
            grade_level,
            subject,
            topic,
            learning_objective,
        ]

        if not all(
            field.strip()
            for field in required_fields
        ):

            st.warning(
                "Please fill Grade Level, Subject, Topic and Learning Objective."
            )

            st.stop()

        if clarification_required == "Yes":

            if not st.session_state.get(
                "answers",
                [],
            ):

                st.warning(
                    "Please answer and save the clarification questions before generating the lesson plan."
                )

                st.stop()

        log_event("REQUIREMENTS_SUBMITTED")
        with st.spinner(
            "Generating lesson plan..."
        ):

            try:

                lesson_plan = generate_lesson_plan(

                    **inputs,

                    questions_list=questions_list,

                    answers=answers,

                )

                if not lesson_plan:

                    st.error(
                        "Unable to generate lesson plan."
                    )

                    st.stop()

                st.session_state.lesson_plan = lesson_plan

                # Save the original AI-generated lesson
                st.session_state.initial_lesson = lesson_plan

                log_event(
                    "LESSON_GENERATED"
                )
                save_research_session(
    inputs=inputs,
    lesson_plan=lesson_plan,
    teacher_prior_knowledge=prior_knowledge,
    teacher_misconceptions=misconceptions,
    teacher_learning_difficulties=learning_difficulties,
)

            except Exception as e:

                st.error(f"Error: {e}")

                st.stop()

        # =================================================
        # AI QUALITY REVIEW
        # =================================================

        with st.spinner(
            "Reviewing lesson quality..."
        ):

            try:

                quality_review = review_lesson_plan(

                    lesson_plan,

                    framework,

                )

                st.session_state.lesson_review = quality_review
                log_event(
                    "EVALUATION_GENERATED"
                )

            except Exception:

                st.warning(
                    "Lesson plan generated successfully, but AI Evaluation could not be completed."
                )

                st.session_state.lesson_review = ""

        st.success(
            "Lesson plan generated successfully."
        )

        st.info(
            "Scroll down to review and edit the lesson plan."
        )

        st.rerun()