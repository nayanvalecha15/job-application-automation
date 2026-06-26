import re

# ── Salary Extractor ──────────────────────────────────
# IN  → job description text
# DO  → finds all salary mentions
# OUT → list of salaries found

def extract_salary(text):
    pattern  = r"\d+(?:-\d+)?\s*LPA"
    salaries = re.findall(pattern, text)
    return salaries


# ── Experience Extractor ──────────────────────────────
# IN  → job description text
# DO  → finds experience requirements
# OUT → list of experience mentions

def extract_experience(text):
    pattern = r"\d+(?:-\d+)?\s*(?:years?|yrs?)"
    exp     = re.findall(pattern, text)
    return exp


# ── Email Extractor ───────────────────────────────────
# IN  → any text
# DO  → finds all email addresses
# OUT → list of emails found

def extract_emails(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails  = re.findall(pattern, text)
    return emails


# ── Test all three ────────────────────────────────────
jd = """
We offer 8-12 LPA for this role.
Senior candidates can expect 15 LPA.
Requirements: 3-5 years of Python experience.
Freshers with 1 year experience also welcome.
Contact us at jobs@hypothesisbase.com or hr@navapbc.com
"""

print("Salaries found    :", extract_salary(jd))
print("Experience found  :", extract_experience(jd))
print("Emails found      :", extract_emails(jd))

test_text = "We offer 8-12 LPA and require 3-5 years experience."
print(extract_salary(test_text))      # should print "8-12 LPA"
print(extract_experience(test_text))  # should print "3-5 years"