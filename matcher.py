import re
from resume_keywords import RESUME_KEYWORDS

FAANG_COMPANIES = ["Meta", "Facebook", "Amazon", "Apple", "Netflix", "Google", "Alphabet", "Microsoft", "Walmart"]

def is_faang(company_name: str) -> bool:
    if not company_name: return False
    company_name = company_name.lower()
    for f in FAANG_COMPANIES:
        if f.lower() in company_name:
            return True
    return False

def is_security_clearance(description: str) -> bool:
    """
    Returns True if the description mentions security clearance requirements.
    """
    if not description: return False
    description = description.lower()
    clearance_keywords = [
        "security clearance", "clearance required", "ts/sci", 
        "top secret", "polygraph", "public trust", "secret clearance"
    ]
    for kw in clearance_keywords:
        if kw in description:
            return True
    return False

def is_senior_title(title: str) -> bool:
    """
    Returns True if the title contains senior-level keywords.
    Filters out Principal, Staff, Director, VP, and other senior roles.
    Now includes 'lead' and 'manager' as requested.
    """
    if not title: return False
    title_lower = title.lower()
    senior_keywords = [
        "principal", "staff", "director", "vp", "vice president", 
        "head of", "chief", "senior director", "senior principal",
        "lead", "manager"
    ]
    return any(kw in title_lower for kw in senior_keywords)

def is_rejected_stack(title: str, description: str) -> bool:
    """
    Returns True if the role is a 'java fullstack' role.
    """
    title_lower = title.lower()
    desc_lower = description.lower()
    
    # Check for "java" and "fullstack" together
    if "java" in title_lower and "fullstack" in title_lower:
        return True
    if "java" in desc_lower and "fullstack" in desc_lower:
        return True
    return False

def has_high_experience_requirement(description: str) -> bool:
    """
    Returns True if the description mentions experience years > 8.
    Matches patterns like '10+ years', '12 years of experience', etc.
    """
    # Look for patterns like "10+ years", "9 years", "minimum 12 years"
    matches = re.findall(r'(\d+)\+?\s*years?', description, re.IGNORECASE)
    if matches:
        for m in matches:
            try:
                val = int(m)
                # Filter out obvious non-experience numbers (e.g., "401k", "100% remote") 
                # strictly looking for "X years", but context matters. 
                # Assuming regex (\d+ years) captures mostly experience in this context.
                # Threshold > 8 per user request
                if val > 7 and val < 30: # reasonable cap to avoid false positives like "Fortune 500"
                    return True
            except ValueError:
                continue
    return False

def score_job(job: dict) -> dict:
    title = str(job.get("job_title") or "").lower()
    description = str(job.get("job_description") or "").lower()
    employer = str(job.get("employer_name") or "")
    location = str(job.get("job_city") or "") + " " + str(job.get("job_country") or "")
    apply_link = str(job.get("job_apply_link") or job.get("job_google_link") or "")
    posted_at = str(job.get("job_posted_at_datetime_utc") or "Unknown")

    # Keyword match score
    matched = [kw for kw in RESUME_KEYWORDS if kw.lower() in description or kw.lower() in title]
    score = round((len(matched) / len(RESUME_KEYWORDS)) * 100, 1)

    return {
        "title": job.get("job_title"),
        "company": employer,
        "location": location.strip(),
        "posted_at": posted_at,
        "score": score,
        "matched_keywords": matched[:10],  # top 10 to display
        "apply_link": apply_link,
        "description": description # Pass through for debugging if needed
    }


def rank_jobs(jobs: list, min_score: float = 5.0) -> list:
    filtered_jobs = []
    
    print(f"Filtering {len(jobs)} jobs...")
    for job in jobs:
        # 1. Senior Title Filter (NEW - excludes Principal, Staff, Director, etc.)
        title = str(job.get("job_title") or job.get("title") or "")
        if is_senior_title(title):
            # print(f"Skipping Senior Title: {title}")
            continue

        # 2. FAANG Filter
        company = str(job.get("employer_name") or job.get("company") or "")
        if is_faang(company):
            # print(f"Skipping FAANG: {job.get('job_title')} at {company}")
            continue

        # 3. Experience Filter
        description = str(job.get("job_description") or job.get("description") or "")
        if has_high_experience_requirement(description):
            # print(f"Skipping Senior (>8 yrs): {job.get('job_title')}")
            continue

        # 4. Security Clearance Filter
        if is_security_clearance(description):
            # print(f"Skipping Security Clearance job: {job.get('job_title')}")
            continue

        # 5. Stack Filter (NEW - avoids 'java fullstack')
        if is_rejected_stack(title, description):
            # print(f"Skipping rejected stack: {title}")
            continue

        # 6. Score
        scored = score_job(job)
        if scored["score"] >= min_score:
            filtered_jobs.append(scored)

    ranked = sorted(filtered_jobs, key=lambda x: x["score"], reverse=True)
    return ranked
