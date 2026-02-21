from datetime import date, datetime, timedelta
import os
import json # Moved up for clarity

def save_jobs_to_note(jobs: list):
    """
    Writes the ranked jobs to a markdown file.
    """
    today = date.today().strftime("%Y-%m-%d")
    
    # Ensure outputs directory exists
    output_dir = "daily_matches"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filename = os.path.join(output_dir, f"job_matches_{today}.md")
    
    # Markdown header
    content = f"# 🎯 Daily Job Matches — {today}\n\n"
    content += f"**Total Jobs Found:** {len(jobs)}\n"
    content += "Jobs posted in the last 24 hours, ranked by resume match score.\n\n"
    content += "---\n\n"
    
    for i, job in enumerate(jobs, 1):
        score = job.get('score', 0)
        title = job.get('title', 'N/A')
        company = job.get('company', 'N/A')
        location = job.get('location', 'N/A')
        link = job.get('apply_link', '#')
        keywords = ", ".join(job.get('matched_keywords', []))
        
        content += f"## {i}. {title} @ {company}\n"
        content += f"**Match Score:** {score}%\n\n"
        content += f"📍 **Location:** {location}\n\n"
        content += f"🔑 **Keywords:** {keywords}\n\n"
        content += f"[Apply Here]({link})\n\n"
        content += "---\n\n"

    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Successfully saved {len(jobs)} jobs to {filename}")
    return filename

import pandas as pd

def save_jobs_to_excel(jobs: list):
    """
    Writes the ranked jobs to an Excel file.
    """
    if not jobs:
        return None
        
    today = date.today().strftime("%Y-%m-%d")
    
    # Ensure outputs directory exists
    output_dir = "daily_matches"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filename = os.path.join(output_dir, f"job_matches_{today}.xlsx")
    
    # Prepare data for DataFrame
    df_data = []
    for job in jobs:
        df_data.append({
            "Title": job.get("title"),
            "Company": job.get("company"),
            "Location": job.get("location"),
            "Match Score (%)": job.get("score"),
            "Matched Keywords": ", ".join(job.get("matched_keywords", [])),
            "Posted At": job.get("posted_at"),
            "Apply Link": job.get("apply_link")
        })
    
    df = pd.DataFrame(df_data)
    
    # Write to Excel
    df.to_excel(filename, index=False)
    
    print(f"Successfully saved {len(jobs)} jobs to {filename}")
    return filename

import json

def load_history():
    """
    Loads previously matched job URLs from a JSON file.
    """
    history_file = os.path.join("daily_matches", "history.json")
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                return set(json.load(f))
        except Exception as e:
            print(f"⚠️ Error loading history: {e}")
    return set()

def save_history(urls: set):
    """
    Saves matched job URLs to history.json.
    """
    history_file = os.path.join("daily_matches", "history.json")
    try:
        with open(history_file, "w") as f:
            json.dump(list(urls), f, indent=4)
    except Exception as e:
        print(f"⚠️ Error saving history: {e}")

def update_readme(today_str, md_file, excel_file, new_jobs):
    """
    Updates the repository README.md with a 4-day rolling window of jobs.
    """
    readme_path = os.path.join("..", "README.md")
    if not os.path.exists(readme_path):
        readme_path = "README.md"
    
    active_jobs_file = os.path.join("daily_matches", "active_jobs.json")
    
    # Load existing active jobs
    active_jobs = []
    if os.path.exists(active_jobs_file):
        try:
            with open(active_jobs_file, "r") as f:
                active_jobs = json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading active jobs: {e}")

    # Merge new jobs (avoiding duplicates by apply_link)
    seen_urls = {j.get('apply_link') for j in active_jobs if j.get('apply_link')}
    for job in new_jobs:
        if job.get('apply_link') not in seen_urls:
            # Tag with scrapped_date
            job['scrapped_date'] = today_str
            active_jobs.append(job)
    
    # Filter out jobs older than 4 days
    today = datetime.strptime(today_str, "%Y-%m-%d").date()
    filtered_active = []
    for job in active_jobs:
        try:
            scrapped_date_str = job.get('scrapped_date')
            scrapped_date = datetime.strptime(scrapped_date_str, "%Y-%m-%d").date()
            if (today - scrapped_date).days < 4:
                filtered_active.append(job)
        except Exception:
            # If date format is wrong, keep it for safety unless it's clearly old
            filtered_active.append(job)
            
    # Sort by date (newest first) and then score for display
    filtered_active.sort(key=lambda x: (x.get('scrapped_date', ''), x.get('score', 0)), reverse=True)

    # Save back to JSON
    try:
        with open(active_jobs_file, "w") as f:
            json.dump(filtered_active, f, indent=4)
    except Exception as e:
        print(f"⚠️ Error saving active jobs: {e}")

    # Generate README content
    rel_md = f"job-alert/{md_file}"
    rel_excel = f"job-alert/{excel_file}"

    header = "# 🚀 Indeed Job Scraper AI\n\n"
    stats = f"### 📊 Latest Update: {today_str}\n"
    stats += f"- **New Matches Found in Last Run:** {len(new_jobs)}\n"
    stats += f"- **Total Active Matches (Last 4 Days):** {len(filtered_active)}\n"
    stats += f"- 📄 [Full Markdown Report]({rel_md})\n"
    stats += f"- 📁 [Excel Report]({rel_excel})\n\n"
    
    if filtered_active:
        stats += "#### 🎯 Rolling Window: Matches from last 4 days\n\n"
        stats += "| Company | Role | Location | Match Score | Application | Date Found |\n"
        stats += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        
        for job in filtered_active:
            title = job.get('title', 'N/A')
            company = job.get('company', 'N/A')
            location = job.get('location', 'N/A')
            url = job.get('apply_link', '#')
            score = f"{job.get('score', 0)}%"
            scrapped_at = job.get('scrapped_date', 'Unknown')
            app_link = f"[Apply 🚀]({url})"
            stats += f"| **{company}** | {title} | {location} | {score} | {app_link} | {scrapped_at} |\n"
    
    stats += "\n---\n\n"
    stats += "## 📂 Historical Matches\n"
    stats += "All previous matches can be found in the [daily_matches/](job-alert/daily_matches/) folder.\n"

    with open(readme_path, "w") as f:
        f.write(header + stats)
    
    print(f"✅ README.md updated with 4-day rolling window ({len(filtered_active)} jobs)")

