import asyncio
from celery import shared_task
from .utils import fetch_and_store_news

@shared_task
def fetch_news_task(category):
    fetch_and_store_news(category)