import pdfplumber
import openpyxl
from google import genai
from pathlib import Path
# REMOVED: from fpdf import FPDF
# ADDED: ReportLab imports for clean text layout
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from dotenv import load_dotenv
import os
import time

# load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client  = genai.Client(api_key=API_KEY)

# file paths
RESUME_PATH = Path("C:/Users/sw/Downloads/Nayan_resume.pdf")
EXCEL_PATH  = Path("C:/Users/sw/Downloads/nayan_jobs.xlsx")
RESUMES_DIR = Path("C:/Users/sw/Downloads/resumes")


# Function 1
# IN  → path to resume PDF
# DO  → opens PDF, reads every page
# OUT → resume text as string

def read_resume(resume_path):
    text = ""
    with pdfplumber.open(resume_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


# Function 2
# IN  → excel file path
# DO  → finds APPLY and REVIEW jobs
# OUT → list of jobs

def get_apply_jobs(excel_path):
    workbook = openpyxl.load_workbook(excel_path)
    sheet    = workbook.active
    jobs     = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[10] in ["APPLY", "REVIEW"]:
            jobs.append({
                "title"  : row[0],
                "company": row[1],
                "skills" : row[6],
                "score"  : row[9],
                "verdict": row[10]
            })

    return jobs


# Function 3
# IN  → resume text + one job
# DO  → sends to Gemini, rewrites summary and skills
# OUT → tailored resume text
def tailor_resume(resume_text, job):
    python_profile = """
    CANDIDATE TECH PROFILE ADDENDUM:
    - Target Roles: Entry-level Python Developer, AI Automation Specialist, Data Analyst, Business Analyst (100% Remote).
    - Core Tech Learned: Python (Functions, Exception Handling, File Automation, Web Scraping, openpyxl, pathlib, API integrations), SQL (Relational database queries, report generation).
    - Completed Automation Projects:
      1. Automated Job Application Assistant (Python): Built a multi-stage automation pipeline using pdfplumber to read resumes, openpyxl to iterate through excel job leads, and Google Gemini API to dynamically tailor summaries and skill sections.
      2. File System Automation Tool (Python): Created a batch script using pathlib and datetime to automatically clean, timestamp, deduplicate, and sort messy server filenames across directories.
      3. Logic & Dictionary Word Counter (Python): Engineered a custom text processor implementing advanced dictionary logic to track, count, and identify frequency metrics of text strings without external libraries.
    - Career Pivot Strategy: Merge 4 years of digital marketing data analytics, stakeholder communication, and business understanding with fresh, production-ready Python automation skills.
    """

    prompt = f"""You are a professional resume writer specializing in career transitions from business roles to technical roles.

Here is the candidate's core background resume:
{resume_text}

Here is the technical profile addendum of their Python/Automation capabilities:
{python_profile}

Here is the job they are applying for:
Title   : {job['title']}
Company : {job['company']}
Skills  : {job['skills']}

TASK:
Rewrite only the Summary and Skills sections to smoothly bridge their 4 years of business/analytics experience with the technical requirements of this specific job description. Emphasize their automation mindset and project experience.

IMPORTANT RULES:
- Return plain text only
- No asterisks, no bullet points, no markdown
- No ** or * characters anywhere
- Write skills as a comma separated list
- Keep everything completely honest—do not invent data or add skills the candidate doesn't have.

Format exactly like this:

SUMMARY
Write the summary paragraph here.

SKILLS
skill1, skill2, skill3, skill4
"""

    response = client.models.generate_content(
        model    = "models/gemini-2.5-flash",
        contents = prompt
    )

    time.sleep(3)
    return response.text


# Function 4 (UPDATED TO REPORTLAB)
# IN  → tailored text + company name
# DO  → creates resumes folder, saves as PDF using ReportLab
# OUT → PDF saved as Nayan_Valecha_CompanyName.pdf
def save_resume(tailored_text, company):
    RESUMES_DIR.mkdir(exist_ok=True)

    filename = f"Nayan_Valecha_{company.replace(' ', '_')}.pdf"
    filepath = RESUMES_DIR / filename

    # 1. Setup document container with 0.75 inch (54 points) margins
    doc = SimpleDocTemplate(str(filepath), pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []
    
    # 2. Grab standard styles and set up a clean body style
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16, # Controls line spacing so text doesn't overlap
        spaceAfter=10
    )

    # 3. Process the AI text line by line
    for line in tailored_text.split("\n"):
        clean_line = line.strip()
        
        # Format section titles cleanly
        if clean_line in ["SUMMARY", "SKILLS"]:
            title_style = ParagraphStyle(
                'SectionTitle',
                parent=body_style,
                fontName='Helvetica-Bold',
                fontSize=12,
                spaceBefore=12,
                spaceAfter=6
            )
            story.append(Paragraph(clean_line, title_style))
        elif clean_line:
            # ReportLab handles auto-wrapping for long text blocks inside a Paragraph
            story.append(Paragraph(clean_line, body_style))
        else:
            # Empty lines become small visual spacers
            story.append(Spacer(1, 6))

    # 4. Build the actual PDF file
    doc.build(story)
    print(f"Saved: {filename}")


# Run everything
def run():
    print("Reading resume...")
    resume_text = read_resume(RESUME_PATH)

    print("Finding APPLY and REVIEW jobs...")
    jobs = get_apply_jobs(EXCEL_PATH)
    print(f"Found {len(jobs)} jobs to tailor")

    for job in jobs:
        print(f"Tailoring for {job['company']}...")
        tailored = tailor_resume(resume_text, job)
        save_resume(tailored, job["company"])

    print("Done. Check your resumes folder.")

run()