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

def update_readme(today, md_file, excel_file, matches_count):
    """
    Updates the repository README.md with the latest run results.
    """
    # README often exists in the root of the repo (one level up from job-alert usually, but let's check)
    # The user repo structure has job-alert as a subfolder.
    readme_path = os.path.join("..", "README.md")
    
    # If not found in parent, try local
    if not os.path.exists(readme_path):
        readme_path = "README.md"

    # Use relative paths for links in README
    # md_file and excel_file are like "daily_matches/job_matches_2026-02-20.md"
    # From README.md in root, this is "job-alert/daily_matches/..."
    rel_md = f"job-alert/{md_file}"
    rel_excel = f"job-alert/{excel_file}"

    header = "# 🚀 Indeed Job Scraper AI\n\n"
    stats = f"### 📊 Latest Update: {today}\n"
    stats += f"- **New Matches Found Today:** {matches_count}\n"
    stats += f"- 📄 [Markdown Report]({rel_md})\n"
    stats += f"- 📁 [Excel Report]({rel_excel})\n\n"
    stats += "---\n\n"
    stats += "## 📂 Historical Matches\n"
    stats += "All previous matches can be found in the [daily_matches/](job-alert/daily_matches/) folder.\n"

    # If README doesn't exist, create it with the header
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as f:
            f.write(header + stats)
    else:
        # If it exists, we could either overwrite or prepend. Let's overwrite the top summary section.
        with open(readme_path, "w") as f:
            f.write(header + stats)
    
    print(f"✅ README.md updated at {readme_path}")

