import streamlit as st

from session_manager import (
    initialize_session_state,
)

from phase1_requirement_gathering import (
    render_phase1,
)

from phase2_refinement_loop import (
    render_phase2,
)

from phase3_satisfaction_rating import (
    render_phase3,
)

st.set_page_config(
    page_title="Teacher-in-the-Loop AI Lesson Planning Assistant",
    layout="wide",
)

initialize_session_state()

# =====================================================
# HEADER
# =====================================================

st.title("Teacher-in-the-Loop AI Lesson Planning Assistant")

st.caption(
    "Human-AI Collaborative Lesson Design Platform"
)

st.divider()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("Session Status")

    st.write(
        f"Refinement Rounds: "
        f"{st.session_state.refinement_round}"
    )

    if st.session_state.get("lesson_plan", ""):

        st.success(
            "Lesson Plan Generated"
        )

    else:

        st.info(
            "Lesson Plan Not Generated"
        )

    if st.session_state.get(
        "show_phase3",
        False
    ):

        st.success(
            "Satisfaction Phase Reached"
        )

# =====================================================
# PROGRESS TRACKER
# =====================================================

phase1_complete = bool(
    st.session_state.get(
        "lesson_plan",
        ""
    )
)

phase2_complete = (
    st.session_state.refinement_round > 0
)

phase3_complete = (
    st.session_state.get(
        "satisfied",
        False
    )
)

st.subheader("Workflow Progress")

col1, col2, col3 = st.columns(3)

with col1:

    if phase1_complete:
        st.success(
            "✓ Requirements & Lesson Plan"
        )
    else:
        st.info(
            "Phase 1: Requirements Collection"
        )

with col2:

    if phase2_complete:
        st.success(
            "✓ Refinement Completed"
        )
    else:
        st.info(
            "Phase 2: Refinement"
        )

with col3:

    if phase3_complete:
        st.success(
            "✓ Satisfaction & Rating"
        )
    else:
        st.info(
            "Phase 3: Satisfaction"
        )

st.divider()

# =====================================================
# PHASES
# =====================================================

render_phase1()

render_phase2()

render_phase3()