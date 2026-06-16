import streamlit as st
from google import genai
import time

API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)


# =====================================================
# CENTRALIZED GEMINI WRAPPER
# =====================================================
def call_gemini(prompt, model_name, max_retries=3):

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            return response.text

        except Exception as e:

            print("\n================ ERROR ================\n")
            print(type(e))
            print(e)
            print("\n=======================================\n")

            error_message = str(e)

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
                or "503" in error_message
                or "UNAVAILABLE" in error_message
            ):

                wait_time = 2 ** attempt

                print(
                    f"Gemini temporary error. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise e
    return None

# =====================================================
# CLARIFICATION QUESTIONS
# =====================================================
def generate_clarification_questions(
    grade_level,
    subject,
    topic,
    lesson_duration,
    learning_objective,
    prior_knowledge,
    misconceptions,
    learning_difficulties,
    activity_ideas,
    assessment_ideas,
):

    prompt = f"""
You are an expert instructional designer.

A teacher is planning a lesson with the following details:

Grade Level: {grade_level}
Subject: {subject}
Topic: {topic}
Lesson Duration: {lesson_duration}

Learning Objective:
{learning_objective}

Prior Knowledge:
{prior_knowledge}

Common Misconceptions:
{misconceptions}

Learning Difficulties:
{learning_difficulties}

Teacher Activity Ideas:
{activity_ideas}

Teacher Assessment Ideas:
{assessment_ideas}

Generate exactly 3 reflective clarification questions that will help the teacher think more deeply about:

- Student understanding
- Prior knowledge
- Teaching strategies
- Classroom challenges
- Assessment approaches

Return ONLY the questions.
One question per line.
"""

    return call_gemini(
        prompt,
        "gemini-2.5-flash-lite"
    )
# =====================================================
# PHASE 1
# =====================================================
def generate_lesson_plan(
    grade_level,
    subject,
    topic,
    lesson_duration,
    learning_objective,
    prior_knowledge,
    misconceptions,
    learning_difficulties,
    activity_ideas,
    assessment_ideas,
    questions_list,
    answers,
):

    clarification_info = ""

    for q, a in zip(questions_list, answers):
        clarification_info += f"Question: {q}\nAnswer: {a}\n\n"

    prompt = f"""
You are an expert instructional designer and educational consultant.

Create a detailed lesson plan using the 5E Instructional Model.

Teacher Inputs:

Grade Level: {grade_level}
Subject: {subject}
Topic: {topic}
Lesson Duration: {lesson_duration}

Learning Objective:
{learning_objective}

Prior Knowledge:
{prior_knowledge}

Common Misconceptions:
{misconceptions}

Learning Difficulties:
{learning_difficulties}

Teacher Activity Ideas:
{activity_ideas}

Teacher Assessment Ideas:
{assessment_ideas}

Clarification Responses:
{clarification_info}

Generate the response in the following format:

# Lesson Title

# Learning Objectives

# Engage
Describe how students will be introduced to the topic and motivated to learn.

# Explore
Describe activities through which students investigate or explore the concept.

# Explain
Describe how concepts will be explained and clarified.

# Elaborate
Describe extension activities that deepen understanding and application.

# Evaluate
Describe how student learning will be assessed.

# Materials Required

# Assessment Strategy

# Alternative Activity Suggestions

Provide TWO alternative instructional activities that address the same learning objective but use different teaching approaches.

For each activity include:
- Activity Name
- Brief Description
- Pedagogical Approach Used

# Pedagogical Alignment Explanation

Explain briefly how this lesson aligns with Merrill's First Principles of Instruction.

Use the following headings:

## Problem-Centered
## Activation
## Demonstration
## Application
## Integration

Keep explanations concise and teacher-friendly.
"""

    return call_gemini(
        prompt,
        "gemini-2.5-flash"
    )


# =====================================================
# PHASE 2
# =====================================================
def generate_refinement_questions(
    lesson_plan,
    teacher_feedback,
):

    prompt = f"""
Current Lesson Plan:

{lesson_plan}

Teacher Feedback:

{teacher_feedback}

Generate exactly 3 clarification questions.

Return only questions.
"""

    return call_gemini(
        prompt,
        "gemini-2.5-flash-lite"
    )


def generate_refined_lesson_plan(
    lesson_plan,
    teacher_feedback,
    refinement_questions,
    refinement_answers,
):

    clarification_context = ""

    for q, a in zip(refinement_questions, refinement_answers):
        clarification_context += f"Question: {q}\nAnswer: {a}\n\n"
    
    prompt = f"""
Current Lesson Plan:

{lesson_plan}

Teacher Feedback:

{teacher_feedback}

Additional Clarifications:

{clarification_context}

Generate an improved lesson plan.

Maintain ALL sections of the original structure:

# Lesson Title
# Learning Objectives
# Engage
# Explore
# Explain
# Elaborate
# Evaluate
# Materials Required
# Assessment Strategy
# Alternative Activity Suggestions
# Pedagogical Alignment Explanation

Incorporate the teacher feedback and clarification responses while preserving the 5E structure.
"""

    return call_gemini(
        prompt,
        "gemini-2.5-flash"
    )