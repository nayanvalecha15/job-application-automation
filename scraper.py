import sqlite3
from database import create_database, job_exists, save_job, get_jobs
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re

URL  = "https://www.python.org/jobs/location/telecommute/"
DB_PATH = Path("C:/Users/sw/Downloads/job_finder/jobs.db")


MY_SKILLS = [
    # technical
    "python", "sql", "excel", "automation", "windows", "git",
    # data
    "data analysis", "analytics", "reporting",
    # marketing tools you know
    "google analytics", "api",
    # soft skills
    "communication", "testing",
    # business
    "business", "project management"
]

SKILLS_TO_FIND = [
    "python", "sql", "javascript", "java",
    "git", "docker", "linux", "windows", "aws", "azure",
    "pandas", "numpy", "django", "flask", "fastapi",
    "data analysis", "machine learning", "excel",
    "communication", "testing", "unit testing",
    "automation", "api", "rest api"
]


# ── Chef 1 ────────────────────────────────────────────
def get_page(url):
    headers  = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    return response.text


# ── Helper: remote filter ─────────────────────────────
def is_remote(location):
    if "remote" in location.lower():
        return True
    return False


# ── Chef 2 ────────────────────────────────────────────
def parse_jobs(page_content):
    soup  = BeautifulSoup(page_content, "html.parser")
    cards = soup.select("ol.list-recent-jobs li")
    jobs  = []

    for card in cards:
        title       = card.select_one("h2 a").text.strip()
        raw_company = card.select_one(".listing-company-name").text.strip()
        company     = raw_company.split("  ")[-1].strip()
        location    = card.select_one(".listing-location a").text.strip()
        posted      = card.select_one(".listing-posted").text.strip()
        job_url     = "https://www.python.org" + card.select_one("h2 a")["href"]

        if is_remote(location):
            jobs.append({
                "title"   : title,
                "company" : company,
                "location": location,
                "posted"  : posted,
                "url"     : job_url
            })

    return jobs


# ── Chef 3 ────────────────────────────────────────────
def already_exists(sheet, job_url):
    for row in sheet.iter_rows(values_only=True):
        if job_url in row:
            return True
    return False


# ── Chef 4 ────────────────────────────────────────────
def save_jobs(jobs):
    conn    = sqlite3.connect(DB_PATH)
    added   = 0
    skipped = 0

    for job in jobs:
        if job_exists(conn, job["url"]):
            skipped += 1
        else:
            save_job(conn, job)
            added += 1

    conn.close()
    print(f"Added   : {added} new jobs")
    print(f"Skipped : {skipped} already in file")


# ── JD Analyser functions ─────────────────────────────
def extract_skills(jd_text):
    jd_lower     = jd_text.lower()
    found_skills = []
    for skill in SKILLS_TO_FIND:
        if skill in jd_lower:
            found_skills.append(skill)
    return found_skills

def extract_salary(text):
    pattern  = r"\d+(?:-\d+)?\s*LPA"
    salaries = re.findall(pattern, text)
    if salaries:
        return salaries[0]
    return "Not mentioned"


def extract_experience(text):
    pattern = r"\d+(?:-\d+)?\s*(?:years?|yrs?)"
    exp     = re.findall(pattern, text)
    if exp:
        return exp[0]
    return "Not mentioned"

def calculate_score(jd_skills, my_skills):
    if len(jd_skills) == 0:
        return 0

    # how many of YOUR skills does this job want?
    matches = [s for s in my_skills if s in jd_skills]

    # score = your matching skills / your total skills * 100
    return round(len(matches) / len(my_skills) * 100)

def get_verdict(score):
    if score >= 40:        # lowered from 60
        return "APPLY"
    elif score >= 25:
        return "REVIEW"    # borderline — check manually
    else:
        return "REJECT"


# ── Analyser: updates Excel with scores ───────────────
def analyse_all_jobs():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, url FROM jobs")
    rows = cursor.fetchall()

    for row in rows:
        job_id  = row[0]
        title   = row[1]
        job_url = row[2]

        if job_url is None:
            continue

        print(f"Analysing: {title}")
        page     = get_page(job_url)
        soup     = BeautifulSoup(page, "html.parser")
        jd_text  = soup.get_text()

        jd_skills = extract_skills(jd_text)
        score     = calculate_score(jd_skills, MY_SKILLS)
        verdict   = get_verdict(score)
        salary     = extract_salary(jd_text)        # ← new
        experience = extract_experience(jd_text)    # ← new

        have    = [s for s in jd_skills if s in MY_SKILLS]
        lacking = [s for s in jd_skills if s not in MY_SKILLS]

        cursor.execute("""
            UPDATE jobs SET
                skills_wanted  = ?,
                skills_have    = ?,
                skills_lacking = ?,
                score          = ?,
                salary         = ?,
                experience     = ?,
                verdict        = ?
            WHERE id = ?
        """, (
            ", ".join(jd_skills),
            ", ".join(have),
            ", ".join(lacking),
            score,
            salary,
            experience,
            verdict,
            job_id
        ))

        time.sleep(1)

    conn.commit()
    conn.close()
    print("Analysis complete.")


# ── Run everything ────────────────────────────────────
def run():
    print("Setting up database...")
    create_database()                    # creates db if not exists

    print("Scanning python.org jobs...")
    page_content = get_page(URL)
    jobs         = parse_jobs(page_content)
    save_jobs(jobs)

    print("Running JD analyser...")
    analyse_all_jobs()
    print("Complete. Check jobs.db")

run()
