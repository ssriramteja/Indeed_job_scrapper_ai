# Enable Workday, Greenhouse, and iCIMS Job Scraping

## Quick Setup (5 minutes)

Your job scraper is ready to scrape from Workday, Greenhouse, and iCIMS, but it needs a SerpAPI key to search for jobs on these platforms.

### Step 1: Get Free SerpAPI Key

1. Go to https://serpapi.com/users/sign_up
2. Sign up for a free account
3. Copy your API key from the dashboard
4. **Free tier includes 100 searches/month** (plenty for daily job scraping)

### Step 2: Add Key to Your .env File

```bash
cd /Users/sriramtejasingaraju/Downloads/testtt/job-alert
echo "SERPAPI_KEY=your_actual_api_key_here" >> .env
```

**Replace `your_actual_api_key_here` with your real API key!**

### Step 3: Run the Scraper

```bash
python main.py
```

## What You'll Get

With ATS scraping enabled, you'll get jobs from:
- ✅ Indeed (currently working)
- ✅ ZipRecruiter (currently working)
- ✅ Workday (needs SerpAPI key)
- ✅ Greenhouse (needs SerpAPI key)
- ✅ iCIMS (needs SerpAPI key)

**Expected additional jobs:** 20-50 from ATS platforms

## Current Results (Without ATS)

- **Jobs scraped:** 2,077
- **Matching jobs:** 154
- **Sources:** Indeed + ZipRecruiter only

## Alternative: Manual ATS Search

If you don't want to use SerpAPI, you can manually search these sites:
- Workday: Search `site:myworkdayjobs.com "AI Engineer"`
- Greenhouse: Search `site:boards.greenhouse.io "AI Engineer"`
- iCIMS: Search `site:icims.com "AI Engineer"`
