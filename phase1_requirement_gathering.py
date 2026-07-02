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
)

# =====================================================
# FRAMEWORK DISPLAY NAMES
# =====================================================

FRAMEWORK_DISPLAY = {
    "5E Model": "5E Learning Cycle",
    "BOPPPS": (
        "BOPPPS "
        "(Bridge-In, Objectives, Pre-Assessment, "
        "Participatory Learning, Post-Assessment, Summary)"
    ),
    "Gagne's Nine Events": "Gagné's Nine Events of Instruction",
    "Madeline Hunter": "Madeline Hunter Lesson Plan Model",
}

DISPLAY_TO_KEY = {
    value: key
    for key, value in FRAMEWORK_DISPLAY.items()
}


def render_phase1():

    # ----------------------------------------------------
    # Session Initialization
    # ----------------------------------------------------
    if "session_id" not in st.session_state:

        st.session_state.session_id = create_session_id()

        log_event(
            "SESSION_START"
        )

    if "questions_list" not in st.session_state:
        st.session_state.questions_list = []

    if "answers" not in st.session_state:
        st.session_state.answers = []

    if "lesson_plan" not in st.session_state:
        st.session_state.lesson_plan = ""

    if "lesson_review" not in st.session_state:
        st.session_state.lesson_review = ""

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

    framework_display = st.selectbox(
    "Instructional Framework",
    options=list(FRAMEWORK_DISPLAY.values()),
)

    framework = DISPLAY_TO_KEY[
    framework_display
]

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
    # PRIOR KNOWLEDGE
    # -----------------------------------------------------

    st.markdown("### Prior Knowledge")

    if st.button(
        "Generate Prior Knowledge Suggestions"
    ):

        if not topic.strip():

            st.warning(
                "Please enter the lesson topic first."
            )

        else:

            with st.spinner(
                "Generating suggestions..."
            ):

                try:

                    st.session_state[
                        "prior_knowledge_ai"
                    ] = generate_ai_suggestions(
                        suggestion_type="Prior Knowledge",
                        grade_level=grade_level,
                        subject=subject,
                        topic=topic,
                    )

                except Exception as e:

                    st.error(f"Error: {e}")

    if st.session_state.get(
        "prior_knowledge_ai",
        "",
    ):

        st.success(
            "AI suggestions generated."
        )

        st.text_area(
            "AI Suggested Prior Knowledge",
            value=st.session_state[
                "prior_knowledge_ai"
            ],
            height=180,
            disabled=True,
        )

    prior_knowledge = st.text_area(
        "Additional Prior Knowledge (Optional)"
    )
        # -----------------------------------------------------
    # COMMON MISCONCEPTIONS
    # -----------------------------------------------------

    st.markdown("### Common Misconceptions")

    if st.button(
        "Generate Misconception Suggestions"
    ):

        if not topic.strip():

            st.warning(
                "Please enter the lesson topic first."
            )

        else:

            with st.spinner(
                "Generating suggestions..."
            ):

                try:

                    st.session_state[
                        "misconceptions_ai"
                    ] = generate_ai_suggestions(
                        suggestion_type="Common Misconceptions",
                        grade_level=grade_level,
                        subject=subject,
                        topic=topic,
                    )

                except Exception as e:

                    st.error(f"Error: {e}")

    if st.session_state.get(
        "misconceptions_ai",
        "",
    ):

        st.success(
            "AI suggestions generated."
        )

        st.text_area(
            "AI Suggested Common Misconceptions",
            value=st.session_state[
                "misconceptions_ai"
            ],
            height=180,
            disabled=True,
        )

    misconceptions = st.text_area(
        "Additional Misconceptions (Optional)"
    )

    # -----------------------------------------------------
    # LEARNING DIFFICULTIES
    # -----------------------------------------------------

    st.markdown("### Learning Difficulties")

    if st.button(
        "Generate Learning Difficulty Suggestions"
    ):

        if not topic.strip():

            st.warning(
                "Please enter the lesson topic first."
            )

        else:

            with st.spinner(
                "Generating suggestions..."
            ):

                try:

                    st.session_state[
                        "learning_difficulties_ai"
                    ] = generate_ai_suggestions(
                        suggestion_type="Learning Difficulties",
                        grade_level=grade_level,
                        subject=subject,
                        topic=topic,
                    )

                except Exception as e:

                    st.error(f"Error: {e}")

    if st.session_state.get(
        "learning_difficulties_ai",
        "",
    ):

        st.success(
            "AI suggestions generated."
        )

        st.text_area(
            "AI Suggested Learning Difficulties",
            value=st.session_state[
                "learning_difficulties_ai"
            ],
            height=180,
            disabled=True,
        )

    learning_difficulties = st.text_area(
        "Additional Learning Difficulties (Optional)"
    )

    # =====================================================
    # STORE INPUTS
    # =====================================================

    inputs = {

        "grade_level": grade_level,

        "subject": subject,

        "topic": topic,

        "lesson_duration": lesson_duration,

        "framework": framework,

        "learning_objective": learning_objective,

        "prior_knowledge":
            st.session_state.get(
                "prior_knowledge_ai",
                "",
            )
            + "\n"
            + prior_knowledge,

        "misconceptions":
            st.session_state.get(
                "misconceptions_ai",
                "",
            )
            + "\n"
            + misconceptions,

        "learning_difficulties":
            st.session_state.get(
                "learning_difficulties_ai",
                "",
            )
            + "\n"
            + learning_difficulties,

    }

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
                    log_event("CLARIFICATION_ENABLED")

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
                log_event(
                    "LESSON_GENERATED"
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