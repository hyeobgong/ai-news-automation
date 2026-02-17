"""
AI News Automation - Configuration Module
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

# Configuration
MAX_NEWS_ITEMS = int(os.getenv('MAX_NEWS_ITEMS', 10))
LANGUAGE = os.getenv('LANGUAGE', 'ko')

# RSS Feed URLs for AI news (Korean and International sources)
RSS_FEEDS = [
    'https://www.aitimes.com/rss/allArticle.xml',
    'https://www.techneedle.com/rss/allArticle.xml',
    'https://news.google.com/rss/search?q=AI+인공지능&hl=ko&gl=KR&ceid=KR:ko',
    'https://techcrunch.com/tag/artificial-intelligence/feed/',
]

# Output configuration
OUTPUT_DIR = 'output'
