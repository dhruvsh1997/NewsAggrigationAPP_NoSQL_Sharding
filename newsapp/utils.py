import requests
import logging
from pymongo import MongoClient
from django.conf import settings

logger = logging.getLogger('newsapp')

def fetch_and_store_news(category):
    try:
        API_KEY = settings.NEWS_API_KEY
        url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}&pageSize=50"
        response = requests.get(url)
        data = response.json()

        client = MongoClient("mongodb://localhost:27017/")
        db = client[f"news_{category}_db"]
        for article in data.get("articles", []):
            db.articles.insert_one(article)

        logger.info(f"Fetched {len(data.get('articles', []))} articles for category: {category}")
    except Exception as e:
        logger.exception("Error in utils logic:")
        logger.error('Error in API Working', exc_info=True)
