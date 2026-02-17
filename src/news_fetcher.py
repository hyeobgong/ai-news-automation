"""
AI News Fetcher Module
Fetches news from RSS feeds and news APIs
"""
import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsFetcher:
    """Fetches AI-related news from various sources"""
    
    def __init__(self, rss_feeds: List[str], max_items: int = 10):
        self.rss_feeds = rss_feeds
        self.max_items = max_items
    
    def fetch_from_rss(self) -> List[Dict]:
        """Fetch news from RSS feeds"""
        all_news = []
        
        for feed_url in self.rss_feeds:
            try:
                logger.info(f"Fetching from RSS: {feed_url}")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:self.max_items]:
                    news_item = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', ''),
                        'source': feed.feed.get('title', 'Unknown')
                    }
                    all_news.append(news_item)
                    
                logger.info(f"Fetched {len(feed.entries[:self.max_items])} items from {feed_url}")
            except Exception as e:
                logger.error(f"Error fetching from {feed_url}: {str(e)}")
        
        return all_news
    
    def fetch_news(self) -> List[Dict]:
        """Fetch news from all sources"""
        news_items = self.fetch_from_rss()
        
        # Sort by published date (most recent first)
        news_items.sort(key=lambda x: x.get('published', ''), reverse=True)
        
        # Limit to max_items
        return news_items[:self.max_items]
