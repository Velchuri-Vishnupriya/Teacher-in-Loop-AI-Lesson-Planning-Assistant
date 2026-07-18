from io import BytesIO
import re
import html
from xhtml2pdf import pisa
import markdown


# -------------------------------------------------------
# HTML Helpers
# -------------------------------------------------------

def escape_html(text: str) -> str:
    """Escape special HTML characters."""
    return html.escape(text)


def format_content(lines):
    """
    Converts lesson content into clean HTML while preserving
    paragraphs, bullet lists and numbered lists.
    """

    html_parts = []

    in_ul = False
    in_ol = False

    bullet_pattern = re.compile(r"^[-•*]\s+")
    number_pattern = re.compile(r"^\d+\.\s+")

    for line in lines:

        line = escape_html(line.strip())

        if not line:
            continue

        # -----------------------------------
        # Bullet Lists
        # -----------------------------------

        if bullet_pattern.match(line):

            if in_ol:
                html_parts.append("</ol>")
                in_ol = False

            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True

            item = bullet_pattern.sub("", line)

            html_parts.append(f"<li>{item}</li>")

            continue

        # -----------------------------------
        # Numbered Lists
        # -----------------------------------

        if number_pattern.match(line):

            if in_ul:
                html_parts.append("</ul>")
                in_ul = False

            if not in_ol:
                html_parts.append("<ol>")
                in_ol = True

            item = number_pattern.sub("", line)

            html_parts.append(f"<li>{item}</li>")

            continue

        # -----------------------------------
        # Close Lists
        # -----------------------------------

        if in_ul:
            html_parts.append("</ul>")
            in_ul = False

        if in_ol:
            html_parts.append("</ol>")
            in_ol = False

        # -----------------------------------
        # Bold Labels
        # Teacher:
        # Student:
        # Time:
        # -----------------------------------

        label_match = re.match(r"^([A-Za-z ]+):(.*)$", line)

        if label_match:

            label = label_match.group(1)
            value = label_match.group(2).strip()

            html_parts.append(
                f"<p><b>{label}:</b> {value}</p>"
            )

        else:

            html_parts.append(
                f"<p>{line}</p>"
            )

    if in_ul:
        html_parts.append("</ul>")

    if in_ol:
        html_parts.append("</ol>")

    return "\n".join(html_parts)


# -------------------------------------------------------
# HTML Template
# -------------------------------------------------------

def build_html(lesson_plan: str):

    css = """
    <style>

    @page{
        size:A4;
        margin:22px;
    }

    body{
        font-family:Helvetica, Arial, sans-serif;
        font-size:13px;
        color:#333333;
        line-height:1.7;
        background:#FFFFFF;
    }

    .title{
        background:#1F4E79;
        color:white;
        text-align:center;
        padding:18px;
        font-size:24px;
        font-weight:bold;
    }

    .subtitle{
        text-align:center;
        color:#555555;
        font-size:12px;
        margin-top:8px;
        margin-bottom:20px;
    }

    .section{
        margin-bottom:18px;
        page-break-inside:avoid;
    }

    .section-title{
        background:#EAF4FC;
        color:#1F4E79;
        font-size:16px;
        font-weight:bold;
        padding:8px 12px;
        border-left:6px solid #1F4E79;
    }

    .content{
        border:1px solid #D7D7D7;
        padding:12px;
        background:#FCFCFC;
    }

    .content p{
        margin:0 0 8px 0;
        text-align:left;
    }

    .content ul{
        margin-top:6px;
        margin-bottom:8px;
        padding-left:24px;
    }

    .content ol{
        margin-top:6px;
        margin-bottom:8px;
        padding-left:24px;
    }

    .content li{
        margin-bottom:4px;
    }

    .footer{
        margin-top:28px;
        border-top:1px solid #CCCCCC;
        padding-top:10px;
        text-align:center;
        color:#777777;
        font-size:10px;
    }

    </style>
    """
    html_output = f"""
<html>

<head>
    {css}
</head>

<body>

    <div class="title">
        Teacher-in-the-Loop AI Lesson Plan
    </div>

    <div class="subtitle">
        AI-Powered Lesson Planning Assistant
    </div>

"""
    lines = lesson_plan.split("\n")

    current_heading = None
    current_content = []

    # -------------------------------------------------------
    # Flush Current Section
    # -------------------------------------------------------

    def flush_section():

        nonlocal html_output
        nonlocal current_heading
        nonlocal current_content

        if current_heading is None:
            return

        formatted_content = format_content(current_content)

        html_output += f"""
        <div class="section">

            <div class="section-title">
                {escape_html(current_heading)}
            </div>

            <div class="content">
                {formatted_content}
            </div>

        </div>
        """

    # -------------------------------------------------------
    # Detect Major Headings
    # -------------------------------------------------------

    SECTION_HEADINGS = {
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
}

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.upper() in SECTION_HEADINGS:
            flush_section()

            current_heading = line

            current_content = []

        else:

            current_content.append(line)

    flush_section()

    html_output += """
        <div class="footer">
            <b>Teacher-in-the-Loop AI Lesson Planning Assistant</b><br/>
        </div>

    </body>
    </html>
    """

    return html_output

def build_generic_html(lesson_plan: str):

    css = """
    <style>

    @page{
        size:A4;
        margin:22px;
    }

    body{
        font-family:Helvetica, Arial, sans-serif;
        font-size:13px;
        color:#333333;
        line-height:1.6;
    }

    h1{
        color:#1F4E79;
        text-align:center;
    }

    h2,h3,h4{
        color:#1F4E79;
    }

    table{
        border-collapse:collapse;
        width:100%;
        margin:10px 0;
    }

    table, th, td{
        border:1px solid #888;
    }

    th, td{
        padding:6px;
    }

    ul{
        margin-left:20px;
    }

    </style>
    """

    html_body = markdown.markdown(
        lesson_plan,
        extensions=["tables"]
    )

    return f"""
    <html>

    <head>
    {css}
    </head>

    <body>

    {html_body}

    </body>

    </html>
    """
# -------------------------------------------------------
# PDF Generator
# -------------------------------------------------------

def generate_pdf(lesson_plan):

    html_content = build_html(lesson_plan)

    buffer = BytesIO()

    pdf = pisa.CreatePDF(
        src=html_content,
        dest=buffer,
        encoding="UTF-8"
    )

    if pdf.err:
        raise Exception("PDF generation failed.")

    buffer.seek(0)

    return buffer

def generate_generic_pdf(lesson_plan):

    html_content = build_generic_html(lesson_plan)

    buffer = BytesIO()

    pdf = pisa.CreatePDF(
        src=html_content,
        dest=buffer,
        encoding="UTF-8"
    )

    if pdf.err:
        raise Exception("PDF generation failed.")

    buffer.seek(0)

    return buffer