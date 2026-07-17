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

# =====================================================
# PAGE CONFIG
# =====================================================

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
# LESSON PLANNING WORKFLOW
# =====================================================

st.subheader("Lesson Planning Workflow")

col1, col2, col3, col4 = st.columns([1.4, 1.8, 2.0, 1.4])

with col1:
    with st.container(border=True):
        st.markdown(
            "<div style='text-align:center;'><b>Requirements<br>Collection</b></div>",
            unsafe_allow_html=True
        )

with col2:
    with st.container(border=True):
        st.markdown(
            "<div style='text-align:center;'><b>AI Lesson<br>Generation</b></div>",
            unsafe_allow_html=True
        )

with col3:
    with st.container(border=True):
        st.markdown(
            "<div style='text-align:center;'><b>Teacher Review<br>& Editing</b></div>",
            unsafe_allow_html=True
        )

with col4:
    with st.container(border=True):
        st.markdown(
            "<div style='text-align:center;'><b>Export<br>as PDF</b></div>",
            unsafe_allow_html=True
        )

st.divider()

# =====================================================
# PHASES
# =====================================================

render_phase1()

render_phase2()