import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
GMAIL_ADDRESS    = os.getenv("GMAIL_ADDRESS")
APP_PASSWORD     = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL  = os.getenv("RECIPIENT_EMAIL")
EXCEL_PATH       = Path("C:/Users/sw/Downloads/nayan_jobs.xlsx")

#Function 1
# in ecxel file path
# reads excel, finds jobs with APPLY or REVIEW
# returns list of jobs

def get_jobs_summary(excel_path):
    workbook = openpyxl.load_workbook(excel_path)
    sheet    = workbook.active
    jobs     = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        verdict = row[10]
        if verdict in ["APPLY", "REVIEW"]:
            jobs.append({
                "title"  : row[0],
                "company": row[1],
                "score"  : row[9],
                "verdict": row[10]
            })

    return jobs

# test Function 1
jobs = get_jobs_summary(EXCEL_PATH)
for job in jobs:
    print(job["title"], "→", job["verdict"])


def build_email_body(jobs):
    today       = datetime.now().strftime("%d %B %Y")
    apply_jobs  = [j for j in jobs if j["verdict"] == "APPLY"]
    review_jobs = [j for j in jobs if j["verdict"] == "REVIEW"]

    body  = f"Job Summary - {today}\n"
    body += "=" * 40 + "\n\n"

    body += "APPLY THESE JOBS:\n"
    body += "-" * 20 + "\n"
    for job in apply_jobs:
        body += f"{job['title']} at {job['company']} - Score: {job['score']}\n"

    body += "\nREVIEW THESE JOBS:\n"
    body += "-" * 20 + "\n"
    for job in review_jobs:
        body += f"{job['title']} at {job['company']} - Score: {job['score']}\n"

    body += "\n" + "=" * 40 + "\n"
    body += f"Total jobs found : {len(jobs)}\n"
    body += f"Jobs to apply    : {len(apply_jobs)}\n"
    body += f"Jobs to review   : {len(review_jobs)}\n"

    return body

# test Function 2
body = build_email_body(jobs)
print(body)

def send_email(sender, reciever, subject, body):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = reciever
    message["Subject"] = subject
    message.attach(MIMEText(body.replace("\n", "<br>"), "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, APP_PASSWORD)
        server.sendmail(sender, reciever, message.as_string())
    
    print(f"Email sent to {reciever}")

    # run everything
jobs    = get_jobs_summary(EXCEL_PATH)
body    = build_email_body(jobs)
subject = f"Job Summary - {datetime.now().strftime('%d %B %Y')}"
send_email(GMAIL_ADDRESS, RECIPIENT_EMAIL, subject, body)


