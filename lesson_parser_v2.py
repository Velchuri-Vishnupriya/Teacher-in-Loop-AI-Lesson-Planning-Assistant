import re
from typing import Dict


# ============================================================
# MAIN SECTION HEADERS
# ============================================================

SECTION_HEADERS = [
    "LESSON SNAPSHOT",
    "LEARNING OBJECTIVES",
    "LEARNER SNAPSHOT",
    "TOPIC-SPECIFIC TEACHING STRATEGIES",
    "LESSON FLOW",
    "RESOURCES",
    "ASSESSMENT",
    "REFLECTION",
    "HOMEWORK",
    "TEACHER NOTES",
]


# ============================================================
# BASIC UTILITIES
# ============================================================

def clean_text(text: str) -> str:
    """
    Normalize the lesson text.
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ============================================================
# SPLIT LESSON INTO SECTIONS
# ============================================================

def extract_sections(raw_text: str) -> Dict[str, str]:
    """
    Split the complete lesson using the
    predefined section headings.

    Returns:

    {
        "LESSON SNAPSHOT": "...",
        "LEARNING OBJECTIVES": "...",
        ...
    }
    """

    raw_text = clean_text(raw_text)

    pattern = (
        r"(?=^("
        + "|".join(re.escape(header) for header in SECTION_HEADERS)
        + r")\s*$)"
    )

    parts = re.split(
        pattern,
        raw_text,
        flags=re.MULTILINE
    )

    sections = {}

    i = 1

    while i < len(parts):

        heading = parts[i].strip()

        content = parts[i + 1].strip()
        # Remove duplicated heading if present
        if content.upper().startswith(heading):
            content = content[len(heading):].strip()

        sections[heading] = content

        i += 2

    return sections


# ============================================================
# LESSON SNAPSHOT PARSER
# ============================================================

def parse_snapshot(snapshot_text: str) -> Dict[str, str]:
    """
    Convert Lesson Snapshot into a dictionary.

    Example:

    Title: Force and Motion
    Subject: Science
    Grade: 8
    """

    snapshot = {
        "title": "",
        "subject": "",
        "grade": "",
        "board": "",
        "topic": "",
        "duration": "",
        "framework": "",
    }

    for line in snapshot_text.splitlines():

        line = line.strip()

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if key == "title":
            snapshot["title"] = value

        elif key == "subject":
            snapshot["subject"] = value

        elif key == "grade":
            snapshot["grade"] = value

        elif key in ["board", "board/curriculum"]:
            snapshot["board"] = value

        elif key == "topic":
            snapshot["topic"] = value

        elif key == "duration":
            snapshot["duration"] = value

        elif key == "instructional framework":
            snapshot["framework"] = value

    return snapshot
# ============================================================
# MASTER PARSER
# ============================================================

def parse_lesson_plan_v2(raw_text: str) -> Dict:
    """
    Parses the complete lesson plan.

    Only the Lesson Snapshot is converted into a dictionary.
    Every other section is preserved as raw formatted text so
    that the UI can render it without losing Gemini's formatting.
    """

    sections = extract_sections(raw_text)

    lesson = {

        "snapshot": parse_snapshot(
            sections.get("LESSON SNAPSHOT", "")
        ),

        "learning_objectives": sections.get(
            "LEARNING OBJECTIVES",
            ""
        ),

        "learner_snapshot": sections.get(
            "LEARNER SNAPSHOT",
            ""
        ),

        "teaching_strategies": sections.get(
            "TOPIC-SPECIFIC TEACHING STRATEGIES",
            ""
        ),

        "lesson_flow": sections.get(
            "LESSON FLOW",
            ""
        ),

        "resources": sections.get(
            "RESOURCES",
            ""
        ),

        "assessment": sections.get(
            "ASSESSMENT",
            ""
        ),

        "reflection": sections.get(
            "REFLECTION",
            ""
        ),

        "homework": sections.get(
            "HOMEWORK",
            ""
        ),

        "teacher_notes": sections.get(
            "TEACHER NOTES",
            ""
        )

    }

    return lesson