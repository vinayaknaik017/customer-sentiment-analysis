import requests
from bs4 import BeautifulSoup
import csv

# Example Amazon product review page
url = "https://www.amazon.in/product-reviews/B09G9BL5CP/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Request page content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Extract reviews
reviews = soup.find_all("span", {"data-hook": "review-body"})

# Save reviews to CSV
with open("data/reviews.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["review"])  # CSV header
    for r in reviews:
        text = r.get_text(strip=True)
        writer.writerow([text])

print("✅ Reviews scraped and saved to data/reviews.csv")
