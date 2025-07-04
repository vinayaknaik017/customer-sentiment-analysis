import pandas as pd
import requests
import os

# Load environment variables or hardcode for local testing
endpoint = os.getenv("AZURE_ENDPOINT", "gIiJpcg9DDIo8nM4UrXT5br8SD07JQQJ99BGACYeBjFXJ3w3AAAEACOGZ7fM")
key = os.getenv("AZURE_KEY", "https://textanalytics-vinayak.cognitiveservices.azure.com/")
headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json"
}

# Load customer reviews
df = pd.read_csv("data/reviews.csv")

results = []
for idx, row in df.iterrows():
    text = row["review"]
    documents = {
        "documents": [
            {
                "id": str(idx + 1),
                "language": "en",
                "text": text
            }
        ]
    }

    # Call Azure Text Analytics API
    response = requests.post(
        f"{endpoint}/text/analytics/v3.0/sentiment",
        headers=headers,
        json=documents
    )
    
    sentiment = response.json()["documents"][0]["sentiment"]
    results.append(sentiment)

# Add sentiment column and save
df["sentiment"] = results
df.to_csv("data/sentiment_results.csv", index=False)

print("✅ sentiment_results.csv generated successfully.")
