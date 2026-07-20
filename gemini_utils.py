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


def call_gemini(prompt, model_name=DEFAULT_MODEL, retries=3):
    """
    Sends a prompt to Gemini using the new google-genai SDK.
    """

    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
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

            print("========== RESPONSE ==========")
            print(response)

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
# ============================================================
# Supported Instructional Frameworks
# ============================================================

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


# ============================================================
# Prompt Building Blocks
# ============================================================

ROLE_PROMPT = """
You are an expert instructional designer, curriculum planner,
experienced CBSE educator and teacher educator.

Your responsibility is to design classroom-ready lesson plans
for CBSE schools using the 5E Learning Cycle.

Every lesson must:

• Follow SMART learning objectives.
• Demonstrate Constructive Alignment between objectives,
  activities and assessment.
• Apply Merrill's First Principles of Instruction:
    - Activation
    - Demonstration
    - Application
    - Integration
• Encourage active student participation.
• Promote higher-order thinking wherever appropriate.
• Be practical enough for immediate classroom implementation.

The lesson should support teachers,
not replace their professional judgement.
"""


DESIGN_PRINCIPLES = """
DESIGN PRINCIPLES

1. Educational quality is the highest priority.

2. Every lesson must demonstrate Constructive Alignment.

3. Learning Objectives must be SMART.

4. Activities should directly help achieve the stated objectives.

5. Assessment should evaluate the stated objectives.

6. Apply Merrill's First Principles:
   • Activate prior knowledge.
   • Demonstrate new concepts.
   • Allow guided application.
   • Encourage integration with prior learning.

7. Include engaging classroom activities.

8. Include questioning strategies.

9. Encourage student discussion.

10. Include differentiated instruction wherever appropriate.

11. Avoid unnecessary repetition.

12. Keep explanations concise but educationally rich.

13. Every activity must clearly add instructional value.

14. Produce lesson plans suitable for real classroom teaching.
"""


OUTPUT_PHILOSOPHY = """
The lesson is NOT a report.

The lesson is NOT textbook content.

The lesson should read like a professionally designed lesson
prepared by an experienced teacher.

Although concise, every section should contain enough detail
to immediately guide classroom teaching.

Avoid overly brief bullet points.

Provide meaningful instructional content.
"""

# ============================================================
# Dashboard Content Limits
# ============================================================

CONTENT_LIMITS = """
CONTENT LIMITS

Lesson Snapshot
• One value per field.

Learning Objectives
• Exactly 3 SMART objectives.
• Objectives should include measurable action verbs.

Learner Snapshot
For each subsection:
• 3–5 concise but meaningful bullet points.

Teaching Strategies
Provide 3–5 topic-specific strategies.

For each strategy include:
• Strategy
• Classroom implementation
• Expected learning benefit

Lesson Flow

For every 5E stage include:

• Stage Goal
• Teacher Actions
• Student Activities
• Guiding Questions
• Assessment Check
• Approximate Time

Resources
• 5–8 practical classroom resources.

Assessment
• Include formative assessment throughout.
• End with one meaningful Exit Ticket.

Reflection
• Provide two reflective questions for the teacher.

Homework
• Include one meaningful extension activity.

Teacher Notes
• Include practical implementation tips.
"""

# ============================================================
# Output Contract
# ============================================================

OUTPUT_CONTRACT = """
Generate a complete classroom-ready lesson plan with
well-developed instructional content while maintaining
the required structure.
Return the lesson using ONLY the following headings.

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

Never rename headings.

Never change their order.

Never add extra sections.

Return plain text only.
"""

# ============================================================
# Lesson Generation
# ============================================================
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
    """
    Generates a complete AI lesson plan.

    The lesson is designed for a professional teacher dashboard.
    It prioritizes educational quality while keeping the presentation
    concise, topic-specific and easy to scan.
    """

    # --------------------------------------------------------
    # Framework Stages
    # --------------------------------------------------------

    stages = FRAMEWORK_STAGES.get(
        framework,
        []
    )

    formatted_stages = "\n".join(
        f"- {stage}" for stage in stages
    )

    # --------------------------------------------------------
    # Normalize Teacher Inputs
    # --------------------------------------------------------

    grade_level = str(grade_level).strip()

    subject = str(subject).strip()

    topic = str(topic).strip()

    lesson_duration = str(lesson_duration).strip()
    board = str(board).strip()

    framework = str(framework).strip()

    learning_objective = (
        str(learning_objective).strip()
        if learning_objective
        else "Generate appropriate SMART learning objectives."
    )

    prior_knowledge = (
        str(prior_knowledge).strip()
        if prior_knowledge
        else "Not specified."
    )

    misconceptions = (
        str(misconceptions).strip()
        if misconceptions
        else "Not specified."
    )

    learning_difficulties = (
        str(learning_difficulties).strip()
        if learning_difficulties
        else "Not specified."
    )

    # --------------------------------------------------------
    # Teacher Clarifications
    # --------------------------------------------------------

    clarification_section = ""

    if questions_list:

        clarification_section += (
            "\nADDITIONAL TEACHER CLARIFICATIONS\n\n"
        )

        for i, question in enumerate(questions_list):

            answer = ""

            if answers and i < len(answers):
                answer = answers[i].strip()

            if not answer:
                answer = "Not provided."

            clarification_section += (
                f"Question {i + 1}:\n"
                f"{question}\n"
                f"Teacher Response:\n"
                f"{answer}\n\n"
            )

    # --------------------------------------------------------
    # Teacher Inputs
    # --------------------------------------------------------

    teacher_input = f"""
TEACHER INPUTS

Grade Level:
{grade_level}

Subject:
{subject}

Topic:
{topic}

Lesson Duration:
{lesson_duration}

Board / Curriculum:
{board}

Instructional Framework:
{framework}

Framework Stages:
{formatted_stages}

Teacher Learning Objective:
{learning_objective}

Known Prior Knowledge:
{prior_knowledge}

Known Misconceptions:
{misconceptions}

Known Learning Difficulties:
{learning_difficulties}

{clarification_section}
"""

    # --------------------------------------------------------
    # Prompt Foundation
    # --------------------------------------------------------

    prompt = f"""
{ROLE_PROMPT}

{DESIGN_PRINCIPLES}

{OUTPUT_PHILOSOPHY}
IMPORTANT

Assume every lesson is for:

Board:
CBSE (NCERT)

Instructional Framework:
5E Learning Cycle

Do not generate content for any other curriculum or framework.

{CONTENT_LIMITS}

{teacher_input}
"""
    # --------------------------------------------------------
    # Lesson Generation Instructions (Part B)
    # --------------------------------------------------------

    prompt += """

============================================================
YOUR TASK
============================================================

Generate a complete classroom-ready lesson plan for the teacher.

The lesson should:

• be educationally strong
• be easy to scan
• avoid unnecessary text
• be immediately usable in a classroom
• be suitable for a professional dashboard

Never write long paragraphs.

Prefer concise bullets wherever appropriate.
============================================================
CURRICULUM ALIGNMENT
============================================================

Design the lesson according to the selected Board/Curriculum.

Requirements:

• Align concepts with the selected curriculum.

• Use terminology commonly used in that curriculum.

• Ensure learning objectives reflect curriculum expectations.

• Design classroom activities suitable for that curriculum.

• Generate assessments aligned with that curriculum.

• Do not mix content from different curricula.

• Maintain grade-level appropriateness for the selected board.

============================================================
LESSON SNAPSHOT
============================================================

Generate ONLY the following fields.

Title:
Subject:
Grade:
Board:
Topic:
Duration:
Instructional Framework:

Keep every value short.

============================================================
LEARNING OBJECTIVES
============================================================

Generate EXACTLY THREE SMART learning objectives.

Each objective must:

• start with a measurable Bloom's verb
• be one concise sentence
• be measurable
• align with lesson activities
• align with assessment

Avoid vague objectives.

============================================================
LEARNER SNAPSHOT
============================================================

Generate ONLY the following format exactly.

Prior Knowledge

• Bullet 1
• Bullet 2
• Bullet 3

Misconceptions

• Bullet 1
• Bullet 2
• Bullet 3

Learning Difficulties

• Bullet 1
• Bullet 2
• Bullet 3

Rules

• Use the headings exactly as shown above.

• Leave one blank line after each heading.

• Write one bullet per line and start new bullet point in the next following line.

• Do not place multiple bullets on the same line.

• Maximum 3 bullets under each heading.

• Every point must be topic-specific.

• Avoid generic educational statements.

• Every bullet should be classroom observable.


============================================================
TOPIC-SPECIFIC TEACHING STRATEGIES
============================================================

Generate EXACTLY THREE teaching strategies.

These strategies MUST feel unique to THIS lesson.

Avoid generic strategies like

• Think Pair Share
• Visual Learning
• Collaborative Learning
• Inquiry Learning

unless absolutely necessary.

Good examples:

Photosynthesis

• Leaf Observation
• Chloroplast Diagram Analysis
• Plant Growth Prediction

Electric Circuits

• Circuit Assembly
• Fault Detection
• Current Flow Prediction

Fractions

• Fraction Strip Comparison
• Pizza Slice Demonstration
• Number Line Placement

For every strategy generate

Strategy Title

Description

Rules

• Title should be short.

• Description should be practical.

• Maximum TWO concise sentences.

============================================================
LESSON FLOW
============================================================

The lesson MUST strictly follow ONLY the selected instructional framework.

Generate the lesson using ONLY these framework stages.
Lesson Flow Formatting
Rules

• Place the stage name on its own line.
• Place "Estimated Time" on a separate line.
• Place "Teacher Activities" on a separate line.
• Do not merge headings onto the same line.

For every framework stage, follow this format exactly.

Stage Name

Estimated Time: X minutes

Teacher Activities

• Activity 1
• Activity 2
• Activity 3

============================================================
FORMATTING RULES
============================================================

• Use proper Markdown formatting.

• Every bullet must appear on a separate line.

• Leave one blank line between headings and their content.

• Never place multiple bullet points on the same line.

• Preserve the requested section headings exactly.

"""
    for stage in stages:

        prompt += f"""

============================================================
{stage.upper()}
============================================================

Estimated Time

• Allocate an appropriate amount of time.

• The total time across all stages should approximately equal the teacher's lesson duration.

Teacher Activities

• Maximum 2 concise bullet points.

Student Activities

• Maximum 2 concise bullet points.

Quick Check

• ONE formative assessment question.
"""
    prompt += """

Lesson Flow Rules

• Every stage must be concise.

• Every activity should directly support the learning objectives.

• Teacher actions should focus on facilitation.

• Student actions should promote active participation.

• Activities should be topic-specific.

• Avoid repeating the same activity across stages.

• Keep the lesson practical.

• Do not generate unnecessary explanations.

• The complete lesson flow should be easy to understand within a minute.
Additional Rules

• Use the official stage names of the selected instructional framework exactly as provided.

• Do not rename framework stages.

• Include an Estimated Time for every stage.

• Ensure the sum of all stage durations approximately equals the teacher-specified lesson duration.

• Time allocation should be pedagogically balanced.

============================================================
RESOURCES
============================================================

Generate ONLY resources that genuinely support the lesson.

Teaching Materials

• Maximum five bullets.

Digital Resources

• Include only when genuinely useful.

Worksheets

• Include only if appropriate.

Rules

• Recommend realistic classroom resources.

• Avoid expensive or highly specialized equipment unless essential.

"""
    # --------------------------------------------------------
    # Lesson Generation Instructions (Part C)
    # --------------------------------------------------------
    prompt += """

============================================================
ASSESSMENT
============================================================

Generate assessment methods that directly align with the learning objectives.

Include the following sections.

Quick Checks

• Generate EXACTLY THREE short formative assessment questions.

• Each question should assess understanding during different stages of the lesson.

Exit Ticket

• Generate EXACTLY ONE meaningful exit ticket question.

Rules

• Questions should encourage thinking rather than memorization.

• Keep every question concise.

• Avoid repeating the same concept.

============================================================
REFLECTION
============================================================

Generate EXACTLY TWO teacher reflection prompts.

These prompts should help teachers reflect on

• student engagement

• learning effectiveness

• instructional improvement

Rules

• One sentence each.

• Practical and reflective.

============================================================
HOMEWORK
============================================================

Generate ONE meaningful extension activity.

The homework should

• reinforce classroom learning

• encourage independent thinking

• connect naturally with today's lesson

Avoid repetitive textbook exercises unless appropriate.

============================================================
TEACHER NOTES
============================================================

Generate practical notes that may help the teacher during lesson delivery.

Maximum THREE concise bullet points.

Examples

• differentiation reminders

• classroom management tips

• anticipated misconceptions

• pacing reminders

============================================================
EDUCATIONAL QUALITY CHECKLIST
============================================================

Before finalizing the lesson, ensure that

✓ Learning objectives satisfy SMART principles.

✓ Bloom's Taxonomy is naturally integrated.

✓ Merrill's First Principles are reflected where appropriate.

✓ The selected instructional framework is followed completely.

✓ Prior knowledge is activated.

✓ Misconceptions are addressed.

✓ Learning difficulties are considered.

✓ Activities promote active learning.

✓ Teaching strategies are topic-specific.

✓ Assessment aligns with objectives.

✓ Reflection supports continuous teacher improvement.

✓ Homework meaningfully extends classroom learning.

✓ The lesson is practical for real classroom implementation.

✓ Educational quality is never sacrificed for brevity.

============================================================
FORMATTING REQUIREMENTS
============================================================

Return ONLY the completed lesson plan.

Use EXACTLY these headings.

LESSON SNAPSHOT

LEARNING OBJECTIVES

LEARNER SNAPSHOT

TOPIC-SPECIFIC TEACHING STRATEGIES

LESSON FLOW

RESOURCES

ASSESSMENT

REFLECTION

HOMEWORK

TEACHER NOTES

Never rename headings.

Never change heading order.

Do not add extra sections.

Do not include markdown.

Do not include code blocks.

Do not include explanations.

Return plain text only.

Maintain consistent spacing throughout.

============================================================
FINAL SELF-VALIDATION
============================================================

Before returning the lesson verify that

✓ Every required section is present.

✓ Every framework stage is included.

✓ The lesson strictly follows the selected instructional framework.

✓ Teaching strategies are specific to the lesson topic.

✓ Activities align with learning objectives.

✓ Assessment aligns with objectives.

✓ The lesson is concise.

✓ The lesson is easy to scan.

✓ The lesson is classroom-ready.

Return ONLY the completed lesson plan.

"""

    return call_gemini(
        prompt=prompt,
        model_name=DEFAULT_MODEL
    )
# ============================================================
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

    system_prompt = """
You are an experienced instructional designer and classroom teacher helping another teacher prepare a lesson.

Respond naturally and conversationally.

Ask clarification questions whenever important information is missing.

When the teacher requests a lesson plan, generate a complete, classroom-ready lesson plan.

Continue the conversation naturally using the previous conversation history.
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