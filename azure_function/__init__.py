import azure.functions as func
import logging
import json
import requests

# Replace with your Azure Text Analytics endpoint and key
endpoint = "2ejJxyEVCm80m7nCWE0VDbuGgIiJpcg9DDIo8nM4UrXT5br8SD07JQQJ99BGACYeBjFXJ3w3AAAEACOGZ7fM"
key = "https://textanalytics-vinayak.cognitiveservices.azure.com/"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function triggered.")

    try:
        review = req.params.get('review')
        if not review:
            return func.HttpResponse("Missing 'review' parameter", status_code=400)

        url = f"{endpoint}/text/analytics/v3.0/sentiment"
        headers = {"Ocp-Apim-Subscription-Key": key}
        body = {"documents": [{"id": "1", "language": "en", "text": review}]}

        response = requests.post(url, headers=headers, json=body)
        sentiment = response.json()["documents"][0]["sentiment"]

        return func.HttpResponse(json.dumps({"sentiment": sentiment}), mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
