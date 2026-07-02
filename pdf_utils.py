from io import BytesIO
import re
from xhtml2pdf import pisa


# -------------------------------------------------------
# HTML Template
# -------------------------------------------------------

def build_html(lesson_plan: str):

    css = """
    <style>

    @page{
        size:A4;
        margin:25px;
    }

    body{
        font-family:Helvetica,Arial,sans-serif;
        background:#ffffff;
        color:#333333;
        font-size:12px;
        line-height:1.7;
    }

    .title{
        background:#1F4E79;
        color:white;
        padding:18px;
        text-align:center;
        font-size:26px;
        font-weight:bold;
        border-radius:8px;
        margin-bottom:25px;
    }

    .section{
        margin-top:18px;
        margin-bottom:12px;
        page-break-inside:avoid;
    }

    .section-title{
        background:#D9EAF7;
        color:#1F4E79;
        padding:8px 12px;
        font-size:16px;
        font-weight:bold;
        border-left:6px solid #1F4E79;
        border-radius:5px;
        margin-bottom:8px;
    }

    .content{
        border:1px solid #d9d9d9;
        border-radius:5px;
        padding:12px;
        background:#FAFAFA;
        text-align:justify;
        white-space:pre-wrap;
    }

    .bullet{
        margin-left:20px;
    }

    .footer{
        margin-top:30px;
        text-align:center;
        color:gray;
        font-size:10px;
    }

    </style>
    """

    html = f"""
    <html>

    <head>
    {css}
    </head>

    <body>

    <div class="title">
    AI Lesson Plan
    </div>
    """

    lines = lesson_plan.split("\n")

    current_heading = None
    current_content = []

    def flush_section():

        nonlocal html
        nonlocal current_heading
        nonlocal current_content

        if current_heading is None:
            return

        text = "<br>".join(current_content)

        html += f"""

        <div class="section">

            <div class="section-title">
            {current_heading}
            </div>

            <div class="content">
            {text}
            </div>

        </div>

        """

    heading_pattern = re.compile(r"^[A-Za-z0-9\s()'/-]+:$")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if heading_pattern.match(line):

            flush_section()

            current_heading = line[:-1]

            current_content = []

        else:

            current_content.append(line)

    flush_section()

    html += """

    <div class="footer">
    Generated using Teacher-in-the-Loop AI Lesson Planning Assistant
    </div>

    </body>
    </html>

    """

    return html
# -------------------------------------------------------
# PDF Generator
# -------------------------------------------------------

def generate_pdf(lesson_plan):

    html = build_html(lesson_plan)

    buffer = BytesIO()

    pisa.CreatePDF(
        src=html,
        dest=buffer
    )

    buffer.seek(0)

    return buffer