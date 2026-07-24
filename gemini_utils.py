import streamlit as st
from google import genai
from google.genai import types
import time
# ============================================================
# Gemini Configuration
# ============================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# ============================================================
# Model Configuration
# ============================================================

DEFAULT_MODEL = "gemini-2.5-flash"

GENERATION_CONFIG = {
    "temperature": 0.4,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
}


# ============================================================
# Gemini Wrapper
# ============================================================
DEFAULT_MODEL = "gemini-2.5-flash"

FRAMEWORK_STAGES = {

    "5E Model": [
        "Engage",
        "Explore",
        "Explain",
        "Elaborate",
        "Evaluate"
    ],

    "BOPPPS": [
        "Bridge-in",
        "Objective",
        "Pre-assessment",
        "Participatory Learning",
        "Post-assessment",
        "Summary"
    ],

    "Madeline Hunter": [
        "Anticipatory Set",
        "Objective",
        "Input",
        "Modeling",
        "Check for Understanding",
        "Guided Practice",
        "Independent Practice",
        "Closure"
    ],

    "Gagné's Nine Events": [
        "Gain Attention",
        "Inform Learners of Objectives",
        "Stimulate Recall",
        "Present Content",
        "Provide Guidance",
        "Elicit Performance",
        "Provide Feedback",
        "Assess Performance",
        "Enhance Retention"
    ]
}

def call_gemini(prompt, model_name=DEFAULT_MODEL, retries=3):
    """
    Sends a prompt to Gemini using the new google-genai SDK.
    """
    print("\n" + "=" * 80)

    print("PROMPT PREVIEW:")
    print(prompt[:500])

    print("=" * 80)
    api_key = st.secrets["GEMINI_API_KEY"]
    print("API KEY:", type(api_key), repr(api_key))

    client = genai.Client(
        api_key=api_key
    )


    for attempt in range(retries):

        try:

            print("========== GEMINI REQUEST STARTED ==========")

            start_time = time.time()

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            end_time = time.time()

            print(
                f"========== GEMINI RESPONSE RECEIVED IN {end_time-start_time:.2f} SECONDS =========="
            )
            print("\n========== RESPONSE.TEXT ==========\n")

            if hasattr(response, "text"):
                print(response.text)
            else:
                print("No response.text found")

            print("\n========== END RESPONSE ==========\n")

            if hasattr(response, "text") and response.text:
                return response.text

            return ""
        except Exception as e:

            print("========== GEMINI ERROR ==========")
            print(type(e))
            print(e)

            # Friendly message for Gemini rate limit
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                st.info(
                    "The AI service is currently experiencing high demand.\n\n"
                    "Please wait while we automatically try again..."
                )

            if attempt == retries - 1:
                raise

            time.sleep(2**attempt)

    return ""

def generate_lesson_plan(
    grade_level,
    subject,
    topic,
    lesson_duration,
    board,
    framework,
    learning_objective,
    prior_knowledge,
    misconceptions,
    learning_difficulties,
    questions_list,
    answers,
):

    clarification_section = ""

    if questions_list and answers:
        clarification_pairs = []

        for q, a in zip(questions_list, answers):
            clarification_pairs.append(
                f"{q}\nTeacher Response: {a}"
            )

        clarification_section = "\n\n".join(
            clarification_pairs
        )

    prompt = f"""
You are an experienced instructional designer helping a teacher prepare a classroom lesson.

Generate the complete lesson plan now.

Do NOT analyse, critique, review or provide suggestions.

Output ONLY the lesson plan.

=====================================================================
LESSON INFORMATION
=====================================================================

Grade Level: {grade_level}

Subject: {subject}

Topic: {topic}

Lesson Duration: {lesson_duration}

Board/Curriculum: {board}

Instructional Framework: {framework}

Learning Objective / Key Concept:
{learning_objective}

=====================================================================
TEACHER INPUTS
=====================================================================

Prior Knowledge:
{prior_knowledge}

Common Misconceptions:
{misconceptions}

Learning Difficulties:
{learning_difficulties}
"""

    if clarification_section:
        prompt += f"""

Additional Teacher Clarifications:

{clarification_section}
"""

    prompt += """

=====================================================================
INSTRUCTIONS
=====================================================================

Design a practical, classroom-ready lesson plan that:

• strictly follows the selected instructional framework
• if the framework is 5E, organize the lesson into Engage, Explore, Explain, Elaborate and Evaluate
• incorporates all teacher inputs naturally
• writes 3–5 SMART learning objectives using one measurable Bloom's verb per objective
• aligns learning objectives, teaching activities and assessments (Constructive Alignment)
• applies Merrill's First Principles by:
  - activating prior knowledge
  - using a real-world or meaningful context
  - demonstrating new concepts
  - providing guided student application
  - encouraging reflection and transfer of learning
• addresses misconceptions and learning difficulties
• promotes active student participation
• includes formative assessment during the lesson and a summative assessment at the end
• provides concise teacher notes and reflection prompts

=====================================================================
OUTPUT TEMPLATE
=====================================================================

Begin immediately with the headings below.

## Lesson Snapshot

Provide:
- Lesson Title
- Grade
- Subject
- Topic
- Duration
- Board
- Framework

## Learning Objectives

## Learner Snapshot

Summarize:
- Prior Knowledge
- Common Misconceptions
- Learning Difficulties

## Topic-Specific Teaching Strategies

## Lesson Flow

If the selected framework is 5E, organize as:

### Engage
### Explore
### Explain
### Elaborate
### Evaluate

## Resources

## Assessment

## Reflection

## Homework

## Teacher Notes

Keep the lesson concise, practical and classroom-ready.

Begin directly with:

## Lesson Snapshot
"""

    return call_gemini(prompt)

# AI Clarification Questions
# ============================================================
def generate_clarification_questions(
    grade_level,
    subject,
    topic,
    lesson_duration,
    board,
    framework,
    learning_objective,
    prior_knowledge,
    misconceptions,
    learning_difficulties,
):
    """
    Generates clarification questions only when additional
    teacher input would significantly improve the lesson plan.
    """

    prompt = f"""
You are an experienced instructional designer.

Your task is to identify missing information that would help
generate a higher-quality lesson plan.

============================================================
LESSON INFORMATION
============================================================

Grade:
{grade_level}

Subject:
{subject}

Topic:
{topic}

Duration:
{lesson_duration}
Board / Curriculum:
{board}

Instructional Framework:
{framework}

Learning Objective:
{learning_objective}

Prior Knowledge:
{prior_knowledge}

Misconceptions:
{misconceptions}

Learning Difficulties:
{learning_difficulties}

============================================================
YOUR TASK
============================================================

Generate THREE clarification questions.

The questions should ONLY ask about information that is
currently missing or unclear.

Good examples include:

• classroom size
• available teaching resources
• assessment preferences
• differentiation needs
• technology availability
• language support
• special classroom constraints

Avoid asking questions that are already answered above.

Avoid repeating information.

============================================================
QUESTION RULES
============================================================

Each question should:

• be short
• be specific
• help improve lesson quality
• be easy for teachers to answer

Avoid yes/no questions whenever possible.

============================================================
OUTPUT FORMAT
============================================================

Return only the questions.

One question per line.

Do not number them.

Do not include headings.

Do not include explanations.

Return plain text only.

"""

    return call_gemini(
        prompt=prompt,
        model_name=DEFAULT_MODEL
    )
# ============================================================
# AI Suggestions
# ============================================================

def generate_ai_suggestions(
    suggestion_type,
    grade_level,
    subject,
    topic,
    board
):
    """
    Generates AI suggestions for Phase 1 requirement gathering.

    Supported suggestion types:

    • Prior Knowledge
    • Common Misconceptions
    • Learning Difficulties
    """

    suggestion_rules = {

        "Prior Knowledge": """
Generate EXACTLY 5 concise bullet points describing
what students are likely to already know before
starting this lesson.

Keep every point topic-specific.

Return bullets only.
""",

        "Common Misconceptions": """
Generate EXACTLY 5 common misconceptions students
may have regarding this topic.

The misconceptions should be realistic and
classroom-observable.

Return bullets only.
""",

        "Learning Difficulties": """
Generate EXACTLY 5 learning difficulties students
may face while learning this topic.

Focus on conceptual and cognitive challenges.

Return bullets only.
"""
    }

    instruction = suggestion_rules.get(
        suggestion_type,
        ""
    )

    prompt = f"""
You are an experienced classroom teacher and instructional designer.

Grade
{grade_level}

Subject
{subject}

Topic
{topic}

Suggestion Type
{suggestion_type}

============================================================

{instruction}

============================================================

Rules

• Keep every bullet concise.

• Do not explain the bullets.

• Avoid generic statements.

• Make every point specific to the lesson topic.

• Return plain text only.

"""

    return call_gemini(
        prompt=prompt,
        model_name=DEFAULT_MODEL
    )
# ============================================================
# AI Lesson Review
# ============================================================

def review_lesson_plan(
    lesson_plan,
    framework,
):
    """
    Reviews the generated lesson plan and provides constructive,
    educationally meaningful suggestions for improvement.
    """

    prompt = f"""
You are an expert instructional designer reviewing a teacher's
lesson plan.

Your responsibility is to improve lesson quality while respecting
the teacher's professional judgement.

============================================================
INSTRUCTIONAL FRAMEWORK
============================================================

{framework}

============================================================
LESSON PLAN
============================================================

{lesson_plan}

============================================================
REVIEW CRITERIA
============================================================

Evaluate the lesson using the following criteria.

1. Learning Objectives

• Are they SMART?
• Are they measurable?
• Are they aligned with classroom activities?

------------------------------------------------------------

2. Instructional Framework

• Does the lesson correctly follow the selected framework?
• Are all framework stages present?
• Is the sequence logical?

------------------------------------------------------------

3. Teaching Strategies

• Are the strategies specific to the lesson topic?
• Do they actively engage learners?
• Are they practical for classroom implementation?

------------------------------------------------------------

4. Learner Considerations

• Is prior knowledge activated?
• Are misconceptions addressed?
• Are learning challenges considered?

------------------------------------------------------------

5. Assessment

• Are formative assessments aligned with objectives?
• Does the Exit Ticket measure learning effectively?

------------------------------------------------------------

6. Educational Quality

Consider whether the lesson naturally reflects:

• SMART Objectives
• Bloom's Taxonomy
• Merrill's First Principles`

============================================================
YOUR RESPONSE
============================================================

Provide feedback under ONLY these headings.

Strengths

• Maximum 5 concise bullet points.

Suggestions

• Maximum 5 practical improvement suggestions.

Overall Evaluation

Provide ONE short paragraph summarizing the lesson quality.

============================================================
RULES
============================================================

Do NOT rewrite the lesson.

Do NOT generate a new lesson plan.

Only provide constructive feedback.

If a section is already strong, acknowledge it instead of
suggesting unnecessary changes.

Keep the tone professional, supportive and actionable.

Return plain text only.

Do not include markdown.

"""

    return call_gemini(
        prompt=prompt,
        model_name=DEFAULT_MODEL
    )

# ============================================================
# Generic Conversational LLM
# ============================================================

def chat_with_generic_llm(chat_history):
    """
    Generic conversational interface used for the
    Generic-LLM experimental condition.
    """

    system_prompt = """You are helping a teacher improve an existing lesson plan.

Discuss requested changes naturally.

Explain how the lesson would be improved.

Suggest ideas when appropriate.
Do not organize lessons using predefined instructional frameworks (for example, the 5E model).
Do not regenerate the complete lesson plan unless the teacher explicitly asks for the final lesson plan.

Remember all agreed changes throughout the conversation.
"""

    conversation = system_prompt + "\n\n"

    for message in chat_history:

        role = message["role"]

        if role == "user":

            conversation += f"Teacher:\n{message['content']}\n\n"

        else:

            conversation += f"Assistant:\n{message['content']}\n\n"

    return call_gemini(conversation)

# =====================================================
# AI LESSON REFINEMENT
# =====================================================

def refine_lesson_with_ai(current_lesson, teacher_request):
    """
    Refines an existing lesson plan based on the teacher's request.

    Returns
    -------
    changes_made : str
        The exact content that was added/modified/deleted.

    updated_lesson : str
        The complete updated lesson plan.
    """

    prompt = f"""
You are an expert instructional designer.

A complete lesson plan has already been generated.

Your task is ONLY to refine the lesson according to the teacher's request.

Current Lesson Plan
===================

{current_lesson}

Teacher's Refinement Request
============================

{teacher_request}

Instructions

1. Modify ONLY what the teacher requested.
2. Preserve everything else.
3. Keep the same lesson structure and section headings.
4. Return BOTH the modified content and the complete updated lesson.
5. DO NOT summarize the changes.
6. DO NOT simply say "Lesson updated."
7. Show the ACTUAL modified content exactly as it should appear in the lesson.
8. Return plain text only.

Return your response EXACTLY in this format.

=== CHANGES MADE ===

Show ONLY the content that was added, removed or modified.

If a section was modified, show the updated version of ONLY that section.

=== UPDATED LESSON ===

Return the COMPLETE updated lesson plan.

The updated lesson MUST still contain these headings exactly:

LESSON SNAPSHOT

LEARNING OBJECTIVES

LEARNER SNAPSHOT

TEACHING STRATEGIES

LESSON FLOW

RESOURCES

ASSESSMENT

REFLECTION

HOMEWORK

TEACHER NOTES
"""

    response = call_gemini(prompt)

    changes = ""
    updated_lesson = response

    if "=== UPDATED LESSON ===" in response:

        parts = response.split("=== UPDATED LESSON ===", 1)

        changes = (
            parts[0]
            .replace("=== CHANGES MADE ===", "")
            .strip()
        )

        updated_lesson = parts[1].strip()

    return changes, updated_lesson