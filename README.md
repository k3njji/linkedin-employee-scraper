# linkedin-employee-scraper

> Scrape a LinkedIn company's **People** page into a clean CSV/XLSX — with bot-detection mitigations built in.

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)
![Selenium](https://img.shields.io/badge/selenium-4.x-green?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)

---

## ⚠️ Legal Disclaimer

This tool is intended for **personal, research, or internal use only.**  
Scraping LinkedIn violates their [User Agreement](https://www.linkedin.com/legal/user-agreement). Using this script may result in your account being restricted or banned. **You assume all responsibility for how you use it.**

---

## Features

- Authenticates via your personal `li_at` session cookie — no password handling
- Auto-clicks **"Show more results"** until all employees are loaded
- Full-page lazy-load scroll before scraping so no cards are missed
- Fallback CSS selector chains — resilient to LinkedIn's frequent class-name rotations
- Randomised delays + patched `navigator.webdriver` to reduce bot fingerprint
- Deduplicates on **Profile URL** (not name) for accuracy
- Exports to both **CSV** and **XLSX**
- Structured logging with timestamps throughout

---

## Requirements

- Python 3.10+
- Google Chrome installed
- A valid LinkedIn account (and its `li_at` cookie)

---

## Installation

```bash
git clone https://github.com/k3njji/linkedin-employee-scraper.git
cd li-people-scraper

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

**`requirements.txt`**
```
selenium>=4.0
webdriver-manager
pandas
openpyxl
```

---

## Getting Your `li_at` Cookie

1. Log in to [linkedin.com](https://www.linkedin.com) in Chrome
2. Open DevTools → **Application** → **Cookies** → `https://www.linkedin.com`
3. Find the cookie named `li_at` and copy its **Value**

> This cookie expires periodically. If the script stops working, grab a fresh one.

---

## Usage

Open `linkedin_scraper.py` and fill in the config block at the top:

```python
LI_AT_TOKEN = "your_li_at_cookie_value"
COMPANY_URL  = "https://www.linkedin.com/company/anthropic/people"
OUTPUT_CSV   = "output.csv"
OUTPUT_XLSX  = "output.xlsx"
HEADLESS     = False   # True for background/pipeline runs
```

Then run:

```bash
python linkedin_scraper.py
```

---

## Output

Both files contain the same three columns:

| Column | Description |
|---|---|
| `Name` | Full name as shown on LinkedIn |
| `Bio / Title` | Current role / headline |
| `Profile URL` | Direct link to the employee's profile |

---

## How It Works

```
inject li_at cookie
        │
        ▼
load employee/people/ page
        │
        ▼
click "Show more results" (loop until exhausted)
        │
        ▼
scroll full page (triggers lazy-loaded cards)
        │
        ▼
scrape cards → extract name, bio, URL
        │
        ▼
deduplicate on Profile URL
        │
        ▼
save CSV + XLSX
```

---

## Known Limitations

- **LinkedIn changes its DOM frequently.** The selector fallback chains cover the most common patterns, but a major redesign will require updates.
- **Rate limiting / soft blocks.** Running this on large companies (1000+ employees) in quick succession will likely trigger DataDome. Add longer delays or run in batches.
- **li_at is account-bound.** If LinkedIn flags unusual activity, your account — not just the script — may be restricted.

---

## Project Structure

```
li-people-scraper/
├── linkedin_scraper.py   # Main script
├── requirements.txt
└── README.md
```

---

## License

MIT — do whatever you want, but you're on your own legally.
