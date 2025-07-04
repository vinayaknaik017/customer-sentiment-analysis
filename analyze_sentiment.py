import pandas as pd
import requests
import os

# ✅ Azure Setup
endpoint = os.getenv("AZURE_ENDPOINT", "https://textanalytics-vinayak.cognitiveservices.azure.com")
key = os.getenv("AZURE_KEY", "2ejJxyEVCm80m7nCWE0VDbuGgIiJpcg9DDIo8nM4UrXT5br8SD07JQQJ99BGACYeBjFXJ3w3AAAEACOGZ7fM")
headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json"
}

# ✅ Load reviews from CSV
try:
    df = pd.read_csv("data/reviews.csv")
except FileNotFoundError:
    print("❌ Error: 'data/reviews.csv' not found.")
    exit()

results = []

# ✅ Iterate through each review
for idx, row in df.iterrows():
    text = str(row.get("review", "")).strip()

    # Skip empty text
    if not text:
        results.append("error_empty")
        continue

    documents = {
        "documents": [
            {
                "id": str(idx + 1),
                "language": "en",
                "text": text
            }
        ]
    }

    try:
        response = requests.post(
            f"{endpoint}/text/analytics/v3.0/sentiment",
            headers=headers,
            json=documents
        )

        result = response.json()

        if "documents" in result:
            sentiment = result["documents"][0]["sentiment"]
            results.append(sentiment)
        elif "error" in result:
            print(f"❌ Azure API error for review {idx}: {result['error']['message']}")
            results.append("error_api")
        else:
            print(f"❌ Unexpected response: {result}")
            results.append("error_unknown")

    except Exception as e:
        print(f"❌ Request failed for review {idx}: {str(e)}")
        results.append("error_exception")

# ✅ Save results
df["sentiment"] = results
df.to_csv("data/sentiment_results.csv", index=False)
print("✅ Done! sentiment_results.csv saved in /data folder.")
