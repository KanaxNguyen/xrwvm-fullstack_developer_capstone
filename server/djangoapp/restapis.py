import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "database", "data")


def _load_json(filename, key):
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as file:
        return json.load(file)[key]


def _fallback_get(endpoint):
    if endpoint == "/fetchDealers":
        return _load_json("dealerships.json", "dealerships")
    if endpoint.startswith("/fetchDealers/"):
        state = endpoint.rsplit("/", 1)[1]
        return [dealer for dealer in _load_json("dealerships.json", "dealerships") if dealer.get("state") == state]
    if endpoint.startswith("/fetchDealer/"):
        dealer_id = int(endpoint.rsplit("/", 1)[1])
        return [dealer for dealer in _load_json("dealerships.json", "dealerships") if dealer.get("id") == dealer_id]
    if endpoint == "/fetchReviews":
        return _load_json("reviews.json", "reviews")
    if endpoint.startswith("/fetchReviews/dealer/"):
        dealer_id = int(endpoint.rsplit("/", 1)[1])
        return [review for review in _load_json("reviews.json", "reviews") if review.get("dealership") == dealer_id]
    return {}


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        params = "?" + "&".join([f"{key}={value}" for key, value in kwargs.items()])
    request_url = backend_url + endpoint + params
    try:
        response = requests.get(request_url, timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return _fallback_get(endpoint)


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url.rstrip("/") + "/analyze/" + text
    try:
        response = requests.get(request_url, timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        lowered = text.lower()
        if any(word in lowered for word in ["fantastic", "great", "good", "excellent", "best"]):
            sentiment = "positive"
        elif any(word in lowered for word in ["bad", "poor", "terrible", "worst"]):
            sentiment = "negative"
        else:
            sentiment = "neutral"
        return {"sentiment": sentiment}


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        data = dict(data_dict)
        reviews_path = os.path.join(DATA_DIR, "reviews.json")
        with open(reviews_path, encoding="utf-8") as file:
            payload = json.load(file)
        reviews = payload.setdefault("reviews", [])
        data["id"] = max([review.get("id", 0) for review in reviews] or [0]) + 1
        reviews.append(data)
        with open(reviews_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
        return data

