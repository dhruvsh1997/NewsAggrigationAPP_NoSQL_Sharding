import logging
from django.shortcuts import render
from pymongo import MongoClient
from .tasks import fetch_news_task

logger = logging.getLogger('newsapp')

CATEGORIES = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology', 'world', 'finance', 'politics']

def index(request):
    try:
        selected_category = request.POST.get('category') if request.method == 'POST' else 'business'
        logger.info(f"Category selected: {selected_category}")

        # Trigger async news fetch
        fetch_news_task.delay(selected_category)
        logger.info(f"Dispatched Celery task to fetch news for category: {selected_category}")

        # Connect to the correct shard (DB)
        client = MongoClient("mongodb://localhost:27017/")
        db = client[f"news_{selected_category}_db"]
        articles = list(db.articles.find())

        logger.info(f"Retrieved {len(articles)} articles from DB: news_{selected_category}_db")

        return render(request, 'index.html', {
            'articles': articles,
            'categories': CATEGORIES,
            'selected': selected_category
        })

    except Exception as e:
        logger.exception("Error occurred in index view:")
        logger.error('AAAAAAAAAAAAAAAA', exc_info=True)
        return render(request, 'index.html', {
            'articles': [],
            'categories': CATEGORIES,
            'selected': 'business'
        })