from datetime import date
import os

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

def update_readme(today, md_file, excel_file, jobs):
    """
    Updates the repository README.md with the latest run results, including job details.
    """
    readme_path = os.path.join("..", "README.md")
    if not os.path.exists(readme_path):
        readme_path = "README.md"

    rel_md = f"job-alert/{md_file}"
    rel_excel = f"job-alert/{excel_file}"

    header = "# 🚀 Indeed Job Scraper AI\n\n"
    stats = f"### 📊 Latest Update: {today}\n"
    stats += f"- **New Matches Found Today:** {len(jobs)}\n"
    stats += f"- 📄 [Full Markdown Report]({rel_md})\n"
    stats += f"- 📁 [Excel Report]({rel_excel})\n\n"
    
    # Add top 5 matches directly to README
    if jobs:
        stats += "#### 🎯 Top Matches Today:\n"
        for i, job in enumerate(jobs[:5], 1):
            title = job.get('title', 'N/A')
            company = job.get('company', 'N/A')
            score = job.get('score', 0)
            url = job.get('apply_link', '#')
            stats += f"{i}. **{title}** at **{company}** — Match Score: {score}% ([Apply]({url}))\n"
        
        if len(jobs) > 5:
            stats += f"\n...and {len(jobs) - 5} more matches in the [Full Report]({rel_md}).\n"
    
    stats += "\n---\n\n"
    stats += "## 📂 Historical Matches\n"
    stats += "All previous matches can be found in the [daily_matches/](job-alert/daily_matches/) folder.\n"

    # For the user's specific request "update them daily to read.me.md file with adding the date", 
    # we'll overwrite the main dashboard area.
    with open(readme_path, "w") as f:
        f.write(header + stats)
    
    print(f"✅ README.md updated at {readme_path}")

