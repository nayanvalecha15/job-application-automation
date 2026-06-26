# Job Application Automation System

An end-to-end Python system that automatically finds remote
Python jobs, score them against my skills, tailor my resume
using AI, tracks everything in a database, and emails me a
Weekly summary — built to solve a real problem I personally had
during my own job search.

## Why I Built This

After 4 years in digital marketing, I transitioned into Python
automation and data analytics. While job hunting, I found myself
repeating the same manual process every day: checking multiple
job boards, reading dozens of descriptions, manually comparing
my skills against each one, and rewriting my resume for every
application. So I automated the entire pipeline.

## What It Does

- **Scrapes** remote Python job listings automatically
- **Filters** for remote-only roles
- **Analyzes** each job description and extracts required skills
- **Scores** my fit against each job (APPLY / REVIEW / REJECT)
- **Tailors** my resume for each high-match job using Google
  Gemini's API
- **Stores** everything in a SQLite database with full history
- **Emails** me a weekly summary every Monday morning
- **Runs automatically** on a schedule — zero manual effort

## Tech Stack

| Tool | Purpose |
|------|---------|
| `requests` + `BeautifulSoup` | Web scraping job listings |
| `sqlite3` | Storing jobs, scores, and application status |
| `re` (Regex) | Extracting salary and experience patterns from text |
| `openpyxl` | Excel-based reporting (earlier version) |
| `Google Gemini API` | AI-powered resume tailoring |
| `smtplib` | Automated weekly email summaries |
| `Playwright` | Browser automation for login/form workflows |
| `pathlib`, `datetime` | File handling and scheduling logic |
| Windows Task Scheduler | Running the pipeline automatically every morning |

## Project Structure

```
job_finder/
├── scraper.py        # Finds and scores remote Python jobs
├── database.py       # SQLite database functions
├── tailor.py          # AI-powered resume tailoring (Gemini API)
├── emailer.py          # Weekly email summary automation
├── run_scraper.bat      # Scheduled batch runner
├── search_automation.py  # Playwright browser automation demo
├── job_title_scraper.py   # Playwright dynamic content scraping demo
```

## How It Works

1. `scraper.py` visits job board listings, filters for remote
   roles, and saves new ones to a SQLite database
2. Each job description is analyzed for required skills and
   compared against my own skill set to generate a match score
3. Jobs scoring above a threshold get a tailored resume
   generated automatically via Gemini's API in `tailor.py`
4. `emailer.py` reads the database every week and sends a
   summary email — new jobs found, scores, and verdicts
5. The whole pipeline runs automatically via a scheduled task,
   no manual steps required

## Running It Locally

```bash
pip install requests beautifulsoup4 openpyxl python-dotenv google-genai playwright
playwright install

python scraper.py    # Run the scraper + analyzer
python tailor.py     # Generate tailored resumes
python emailer.py    # Send the email summary
```

You'll need a `.env` file with your own API keys:

```
GEMINI_API_KEY=your_key_here
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
RECIPIENT_EMAIL=your_email@gmail.com
```

## What I Learned Building This

This project took me from knowing basic Python (loops,
functions, conditionals) to building a fully automated, A 
multi-stage system involving web scraping, a database,
API integration, scheduled automation, and browser automation —
all built to solve a problem I genuinely needed solved.
