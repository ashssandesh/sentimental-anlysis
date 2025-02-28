from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import sqlite3
import time
from transformers import pipeline
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Ask for ASIN input
asin = input("Enter the Amazon Product ASIN: ").strip()

# Amazon review URL
amazon_url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_sr"

# Configure Selenium WebDriver
options = Options()
options.add_argument("--start-maximized")  # Run in full-screen mode
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Setup WebDriver with automatic retry
for _ in range(3):  # Retry up to 3 times if session fails
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(amazon_url)
        time.sleep(5)  # Allow time for page to load

        # Scroll multiple times with longer pauses
        for _ in range(15):  # Increase scroll attempts
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait longer

        # Click "See More" if available
        try:
            see_more_buttons = driver.find_elements(By.XPATH, "//span[contains(text(), 'See more')]")
            for button in see_more_buttons:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(3)
        except:
            pass  # No "See More" button found

        # Extract reviews using updated XPath
        reviews = []
        review_elements = driver.find_elements(By.XPATH, "//span[@data-hook='review-body']")
        reviews = [r.text.strip() for r in review_elements if r.text.strip()]

        if not reviews:  # If no reviews found, try alternative selector
            review_elements = driver.find_elements(By.XPATH, "//div[@data-hook='review-collapsed']")
            reviews = [r.text.strip() for r in review_elements if r.text.strip()]

        driver.quit()  # Close the browser properly

        if reviews:
            break  # Exit retry loop if reviews found
    except Exception as e:
        print(f"Error occurred: {e}. Retrying...")

# Check if reviews were found
if not reviews:
    print("No reviews found. Amazon may have blocked the request.")
    exit()

# Load pre-trained sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

# Perform sentiment analysis
results = []
for r in reviews:
    sentiment = sentiment_pipeline(r[:512])[0]["label"]  # Limit text length
    results.append({"review_text": r, "sentiment": sentiment})

# Convert to DataFrame
df = pd.DataFrame(results)

# Store in SQLite Database
conn = sqlite3.connect("amazon_reviews.db")
df.to_sql("reviews", conn, if_exists="replace", index=False)

# Read data and analyze
summary = pd.read_sql("SELECT sentiment, COUNT(*) as count FROM reviews GROUP BY sentiment", conn)
print(summary)

# Generate Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(df["review_text"]))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title(f"Amazon Reviews Word Cloud for ASIN {asin}")
plt.show()

# Close DB connection
conn.close()
