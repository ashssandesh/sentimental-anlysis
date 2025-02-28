# Amazon Product Review Scraper (Selenium + NLP)

This project is a fully automated Amazon Product Review Scraper that:
- Scrapes product reviews from Amazon using Selenium
- Performs sentiment analysis using Hugging Face’s `transformers`
- Stores results in SQLite (`amazon_reviews.db`)
- Generates a Word Cloud to visualize the most common words in reviews

## Features
- Dynamic ASIN Input: Enter any Amazon ASIN to scrape its reviews
- Bot Evasion: Uses real browser interactions to bypass Amazon detection
- Sentiment Analysis (AI/ML): Classifies reviews as Positive, Negative, or Neutral
- Data Storage: Saves extracted reviews into an SQLite database
- Word Cloud Visualization: Highlights frequently mentioned words

## Installation
### Step 1: Install Dependencies
Run the following command in your terminal:
```bash
pip install -r requirements.txt
Step 2: Download ChromeDriver (If Needed)
Ensure Google Chrome is installed.
WebDriver automatically installs using webdriver-manager.
How to Run
Run the script:
bash
Copy
Edit
python review_scraper.py
Enter an Amazon ASIN when prompted:
mathematica
Copy
Edit
Enter the Amazon Product ASIN: B09DG5PGFQ
The script will:

Open Amazon Reviews Page
Extract reviews dynamically
Analyze Sentiment
Store in SQLite
Generate a Word Cloud
Sample Output:

css
Copy
Edit
Sentiment Analysis Summary:
   sentiment  count
0  POSITIVE     21
1  NEGATIVE      6
2  NEUTRAL       4
A Word Cloud will be displayed.


Future Enhancements
Export Data to CSV
Scrape Multiple Pages
Include Star Ratings in Analysis
Automate with Cron Jobs / Task Scheduler
Credits
Selenium: For Web Scraping
Hugging Face Transformers: For Sentiment Analysis
Matplotlib & WordCloud: For Visualization
License
This project is licensed under the MIT License.

