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

            st.error(f"Gemini Error: {e}")

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

                wait_time = 5 * (2 ** attempt)

                print(
                    f"Gemini temporary error. Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                raise e

    return None


# =====================================================
# AI SUGGESTIONS
# =====================================================

def generate_ai_suggestions(
    suggestion_type,
    grade_level,
    subject,
    topic,
):

    prompt = f"""
You are an experienced school teacher and instructional designer.

Generate concise AI suggestions for the following lesson.

Suggestion Type:
{suggestion_type}

Grade Level:
{grade_level}

Subject:
{subject}

Topic:
{topic}

Generate 3 to 5 concise and practical suggestions.

Guidelines:

If the suggestion type is Prior Knowledge:
Generate knowledge or skills students should already possess.

If the suggestion type is Common Misconceptions:
Generate misconceptions students commonly have about the topic.

If the suggestion type is Learning Difficulties:
Generate learning challenges students may face while learning this topic.

Keep every suggestion short, practical and teacher-friendly.

Return ONLY the suggestions.

One suggestion per line.

Do not use markdown.

Do not use bullets.

Do not use numbering.
"""

    return call_gemini(
        prompt,
        "gemini-2.5-flash"
    )

# =====================================================
# CLARIFICATION QUESTIONS
# =====================================================

def generate_clarification_questions(
    grade_level,
    subject,
    topic,
    lesson_duration,
    framework,
    learning_objective,
    prior_knowledge,
    misconceptions,
    learning_difficulties,
):

    prompt = f"""
You are an expert instructional designer.

A teacher is planning a lesson with the following details.

Grade Level:
{grade_level}

Subject:
{subject}

Topic:
{topic}

Lesson Duration:
{lesson_duration}

Instructional Framework:
{framework}

Learning Objective:
{learning_objective}

Prior Knowledge:
{prior_knowledge}

Common Misconceptions:
{misconceptions}

Learning Difficulties:
{learning_difficulties}

Generate exactly 3 reflective clarification questions.

The questions should help the teacher think more deeply about:

Student understanding

Prior knowledge

Teaching strategies

Classroom challenges

Assessment approaches

Ask questions only when additional clarification would genuinely help improve the lesson plan.

Avoid repeating information already provided by the teacher.

Avoid examination-style questions.

Encourage inquiry and reflection.

Return ONLY the questions.

One question per line.

Do not use numbering.

Do not use bullet symbols.

Do not use markdown.
"""

    return call_gemini(
        prompt,
        "gemini-2.5-flash"
    )

# =====================================================
# LESSON PLAN GENERATION
# =====================================================
# =====================================================
# LESSON PLAN GENERATION
# =====================================================

def generate_lesson_plan(
    grade_level,
    subject,
    topic,
    lesson_duration,
    framework,
    learning_objective,
    prior_knowledge,
    misconceptions,
    learning_difficulties,
    questions_list,
    answers,
):

    clarification_info = ""

    for q, a in zip(
        questions_list,
        answers,
    ):

        clarification_info += (
            f"Question: {q}\n"
            f"Answer: {a}\n\n"
        )

    framework_sections = {

        "5E Model": """
Lesson Title:

Learning Objectives:

Engage:

Explore:

Explain:

Elaborate:

Evaluate:
""",

        "BOPPPS": """
Lesson Title:

Learning Objectives:

Bridge-In:

Objectives:

Pre-Assessment:

Participatory Learning:

Post-Assessment:

Summary:
""",

        "Gagne's Nine Events": """
Lesson Title:

Learning Objectives:

Gain Attention:

Inform Learners of Objectives:

Recall Prior Knowledge:

Present Content:

Provide Guidance:

Practice:

Feedback:

Assessment:

Retention and Transfer:
""",

        "Madeline Hunter": """
Lesson Title:

Learning Objectives:

Anticipatory Set:

Objective and Purpose:

Input:

Modeling:

Guided Practice:

Independent Practice:

Closure:
"""
    }

    prompt = f"""
You are an expert instructional designer and experienced classroom teacher.

Create a complete classroom-ready lesson plan.

Instructional Framework:
{framework}

Teacher Inputs

Grade Level:
{grade_level}

Subject:
{subject}

Topic:
{topic}

Lesson Duration:
{lesson_duration}

Learning Objective:
{learning_objective}

Prior Knowledge:
{prior_knowledge}

Common Misconceptions:
{misconceptions}

Learning Difficulties:
{learning_difficulties}

Clarification Responses:
{clarification_info}

Follow this instructional framework exactly.

{framework_sections[framework]}

After completing the framework sections, include the following sections.

Materials Required:

Teaching Strategies:

Recommend ONLY the THREE most suitable teaching strategies for this lesson.

For EACH teaching strategy include the following:

Teaching Strategy 1:

Strategy Name:

Why it is Appropriate:

Briefly explain why this strategy is suitable for the lesson topic, learning objective, and students.

Lesson-specific Implementation:

Clearly explain how the teacher can use this strategy during this lesson.

The implementation must be specific to this lesson topic and should include a practical classroom example.

Repeat the same format for Teaching Strategy 2 and Teaching Strategy 3.

Do NOT recommend more than three strategies.

Avoid generic explanations.

Avoid repeating the same implementation.

Classroom Activities:

Generate engaging classroom activities aligned with the lesson objectives.

Formative Assessment:

Closure:

Alternative Activities:

Generate TWO alternative classroom activities.

For each activity include:

Activity Name:

Brief Description:

Pedagogical Approach Used:

The lesson plan must satisfy ALL of the following.

1.
Learning objectives must follow SMART principles.

2.
Use measurable action verbs such as:

Define

Explain

Describe

Analyze

Compare

Evaluate

Predict

Avoid vague verbs such as:

Understand

Know

Learn

3.
Activate students' prior knowledge naturally throughout the lesson.

4.
Address the provided misconceptions during instruction.

5.
Address the identified learning difficulties using appropriate teaching strategies and classroom support.

6.
Generate engaging classroom activities automatically.

7.
Recommend ONLY THREE teaching strategies.

Each strategy must:

- Be highly relevant to this lesson.
- Include a short explanation of why it is appropriate.
- Include a lesson-specific implementation example.
- Be practical for classroom use.

8.
Generate meaningful formative assessments automatically.

Examples include:

Think-Pair-Share

Exit Ticket

Peer Discussion

Observation

Reflection

Student Explanation

Quick Quiz

9.
Generate a meaningful lesson closure automatically.

10.
Integrate Merrill's First Principles throughout the lesson.

11.
Ensure activities are age appropriate.

12.
Ensure the lesson is practical and ready for classroom implementation.

13.
Maintain clear alignment between learning objectives, classroom activities, teaching strategies, and formative assessment.

IMPORTANT

Return ONLY plain text.

Do NOT use markdown.

Do NOT use:

#

##

*

**

***

-

•

Use simple headings ending with a colon.

Keep formatting clean for direct display and PDF export.
"""

    return call_gemini(
        prompt,
        "gemini-2.5-flash"
    )
# =====================================================
# AI LESSON EVALUATION SUMMARY
# =====================================================

def review_lesson_plan(
    lesson_plan,
    framework,
):

    prompt = f"""
You are an experienced instructional designer.

Review the following lesson plan.

Framework:
{framework}

Lesson Plan:

{lesson_plan}

Your role is to provide a supportive evaluation summary.

The lesson plan has already been generated by an AI assistant and should generally be considered suitable for classroom use.

Review the lesson based on the following aspects.

1. Learning objectives are clear and measurable.

2. The lesson follows the selected instructional framework.

3. Prior knowledge has been considered.

4. Common misconceptions are addressed.

5. Learning difficulties are addressed appropriately.

6. Teaching strategies are suitable for the lesson.

7. Classroom activities actively engage students.

8. Formative assessment is included.

9. The lesson is practical for classroom implementation.

Instructions:

Do NOT assign any score, rating, or grade.

Do NOT use negative words such as:

Fail

Poor

Weak

Unsatisfactory

Begin by highlighting the strengths of the lesson.

If improvements are possible, provide ONLY 2 or 3 optional suggestions written in simple and encouraging language.

Conclude with a short overall evaluation indicating whether the lesson plan is ready for classroom use.

Return the response in the following format.

Evaluation Summary:

Strengths:

...

Optional Suggestions:

...

Overall Evaluation:

This lesson plan is well-structured, aligns with the selected instructional framework, and is suitable for classroom implementation. The suggestions above are optional and may be incorporated based on the teacher's preference.

Return plain text only.

Do NOT use markdown.

Do NOT use bullet symbols.

Use simple headings ending with a colon.
"""

    return call_gemini(
        prompt,
        "gemini-2.5-flash"
    )