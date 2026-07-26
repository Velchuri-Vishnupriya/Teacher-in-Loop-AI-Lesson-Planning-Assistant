import streamlit as st
import pandas as pd
import json
import os
from glob import glob
from datetime import datetime

# --------------------------------------------------
# Configuration
# --------------------------------------------------

JSON_FOLDER = "logs/research"
LOG_FILE = "logs/teacher_activity_log.csv"

st.set_page_config(
    page_title="Research Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Load Functions
# --------------------------------------------------

@st.cache_data
def load_sessions():

    sessions = []

    files = sorted(glob(os.path.join(JSON_FOLDER, "*.json")))

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            data["file_name"] = os.path.basename(file)

            sessions.append(data)

        except Exception:
            continue

    return sessions


@st.cache_data
def load_log():

    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)

    return pd.DataFrame()

# --------------------------------------------------
# Clean Markdown / HTML
# --------------------------------------------------

def clean_text(text):

    if not text:
        return ""

    text = text.replace("<br>", "\n")
    text = text.replace("<br/>", "\n")
    text = text.replace("<br />", "\n")

    text = text.replace("&nbsp;", " ")

    return text


sessions = load_sessions()
log_df = load_log()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📊 Teacher-in-the-Loop Research Dashboard")
if st.button("🔄 Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()
st.caption(
    f"Last Refreshed : {datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')}"
)

st.divider()

# --------------------------------------------------
# Overview
# --------------------------------------------------

generic = 0
scaffolded = 0

for s in sessions:

    condition = str(s.get("condition", "")).lower()

    if condition == "generic":
        generic += 1

    elif condition == "scaffolded":
        scaffolded += 1

c1, c2, c3 = st.columns(3)

c1.metric("Total Sessions", len(sessions))
c2.metric("Generic", generic)
c3.metric("Scaffolded", scaffolded)

st.divider()

# --------------------------------------------------
# Session Table
# --------------------------------------------------

summary = []

for s in sessions:

    lesson = s.get("lesson_inputs", {})

    summary.append({

        "Teacher": s.get("teacher_name", ""),

        "Condition": s.get("condition", ""),

        "Topic": lesson.get("topic", ""),

        "Subject": lesson.get("subject", ""),

        "Grade": lesson.get("grade_level", ""),

        "Framework": lesson.get("instructional_framework", ""),

        "File": s.get("file_name", "")

    })

summary_df = pd.DataFrame(summary)

st.subheader("Research Sessions")

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# --------------------------------------------------
# Activity Log
# --------------------------------------------------

st.subheader("Teacher Activity Log")

search = st.text_input("Search Activity Log")

display_log = log_df.copy()

if search:

    display_log = display_log[
        display_log.astype(str)
        .apply(lambda x: x.str.contains(search, case=False))
        .any(axis=1)
    ]

event_names = {
    "SESSION_START": "Session Started",
    "AI_RESPONSE": "AI Response",
    "USER_MESSAGE": "Teacher Response",
    "SESSION_END": "Session End"
}

if "Event Code" in display_log.columns:

    display_log["Event Code"] = (
        display_log["Event Code"]
        .replace(event_names)
    )

st.dataframe(
    display_log,
    use_container_width=True,
    hide_index=True
)

# ==================================================
# Session Viewer
# ==================================================

st.divider()
st.subheader("Session Details")

if len(sessions) == 0:
    st.info("No research sessions found.")
    st.stop()


# -------------------------------
# Session Dropdown
# -------------------------------

session_options = []

for i, session in enumerate(sessions):

    lesson = session.get("lesson_inputs", {})

    teacher = session.get("teacher_name", "Unknown")

    topic = lesson.get("topic", "No Topic")

    condition = session.get("condition", "")

    session_options.append(
        f"{i+1}. {teacher} | {condition} | {topic}"
    )


selected = st.selectbox(
    "Select a Session",
    range(len(session_options)),
    format_func=lambda x: session_options[x]
)

session = sessions[selected]

lesson_inputs = session.get("lesson_inputs", {})
teacher_additions = session.get("teacher_additions", {})
clarifications = session.get("clarification_questions", [])

# ------------------------------------------------
# Teacher Information
# ------------------------------------------------

st.markdown("## 👤 Teacher Information")

c1, c2 = st.columns(2)

with c1:
    st.write("**Teacher Name:**", session.get("teacher_name", "-"))
    st.write("**Condition:**", session.get("condition", "-"))

with c2:
    st.write("**Timestamp:**", session.get("timestamp", "-"))
    st.write("**Session ID:**", session.get("session_id", "-"))

st.divider()

# ------------------------------------------------
# Lesson Inputs
# ------------------------------------------------

st.markdown("## 📘 Lesson Inputs")

display_inputs = lesson_inputs.copy()

display_inputs.pop("prior_knowledge", None)
display_inputs.pop("misconceptions", None)
display_inputs.pop("learning_difficulties", None)

lesson_df = pd.DataFrame({
    "Field": display_inputs.keys(),
    "Value": display_inputs.values()
})

st.table(lesson_df)

st.divider()

# ------------------------------------------------
# Teacher Additions
# ------------------------------------------------

with st.expander("✍ Teacher Additions", expanded=True):

    if teacher_additions:

        for key, value in teacher_additions.items():

            st.markdown(f"**{key.replace('_',' ').title()}**")

            if value:
                st.write(value)
            else:
                st.write("-")

            st.write("")

    else:
        st.info("No teacher additions available.")

st.divider()

# ------------------------------------------------
# Clarification Questions
# ------------------------------------------------

with st.expander("❓ Clarification Questions", expanded=True):

    if clarifications:

        for i, question in enumerate(clarifications, start=1):

            st.markdown(f"**Question {i}**")

            if isinstance(question, dict):

                st.write(question.get("question", ""))

                if "answer" in question:

                    st.success(question.get("answer", ""))

            else:

                st.write(question)

            st.write("")

    else:

        st.info("No clarification questions.")

st.divider()

# ------------------------------------------------
# Lesson Plan
# ------------------------------------------------

st.markdown("## 📄 Lesson Plan")

lesson_plan = clean_text(session.get("lesson_plan", ""))

if lesson_plan:

    with st.expander("View Lesson Plan", expanded=True):
        st.markdown(lesson_plan)

else:
    st.info("Lesson plan not available.")

