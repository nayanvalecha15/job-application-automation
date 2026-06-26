import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("C:/Users/sw/Downloads/job_finder/jobs.db")


# Function 1
# IN  → nothing
# DO  → creates database and jobs table
# OUT → database ready to use

def create_database():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id             INTEGER PRIMARY KEY,
            title          TEXT,
            company        TEXT,
            location       TEXT,
            posted         TEXT,
            status         TEXT,
            url            TEXT,
            skills_wanted  TEXT,
            skills_have    TEXT,
            skills_lacking TEXT,
            score          INTEGER,
            verdict        TEXT,
            salary         TEXT,
            experience     TEXT,
            date_found     TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database ready.")


# Function 2
# IN  → connection + job URL
# DO  → checks if URL exists in database
# OUT → True if exists, False if not

def job_exists(conn, job_url):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM jobs WHERE url = ?",
        (job_url,)
    )

    result = cursor.fetchone()
    return result is not None


# Function 3
# IN  → connection + one job dictionary
# DO  → inserts job into database
# OUT → job saved

def save_job(conn, job):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO jobs
        (title, company, location, posted,
         status, url, date_found)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        job["title"],
        job["company"],
        job["location"],
        job["posted"],
        "Not Applied",
        job["url"],
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    print(f"Saved: {job['title']} at {job['company']}")


# Function 4
# IN  → verdict filter (APPLY/REVIEW/ALL)
# DO  → reads jobs from database
# OUT → list of matching jobs

def get_jobs(verdict=None):
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if verdict is None:
        cursor.execute("SELECT * FROM jobs")
    else:
        cursor.execute(
            "SELECT * FROM jobs WHERE verdict = ?",
            (verdict,)
        )

    rows = cursor.fetchall()
    conn.close()
    return rows