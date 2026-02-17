"""
AI News Automation - Main Script
Automates the process of fetching, processing, and generating AI news content
"""
import os
import sys
import logging
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import (
    OPENAI_API_KEY,
    RSS_FEEDS,
    MAX_NEWS_ITEMS,
    LANGUAGE,
    OUTPUT_DIR
)
from news_fetcher import NewsFetcher
from content_generator import ContentGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ensure_output_dir():
    """Ensure output directory exists"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logger.info(f"Created output directory: {OUTPUT_DIR}")


def save_article(content: str, filename: str = None):
    """Save generated article to file"""
    ensure_output_dir()
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_news_{timestamp}.md"
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f"Article saved to: {filepath}")
    return filepath


def main():
    """Main execution function"""
    logger.info("Starting AI News Automation...")
    
    # Initialize components
    logger.info(f"Fetching news from {len(RSS_FEEDS)} RSS feeds...")
    fetcher = NewsFetcher(RSS_FEEDS, MAX_NEWS_ITEMS)
    
    # Fetch news
    news_items = fetcher.fetch_news()
    
    if not news_items:
        logger.warning("No news items fetched. Exiting.")
        return
    
    logger.info(f"Successfully fetched {len(news_items)} news items")
    
    # Generate content
    generator = ContentGenerator(OPENAI_API_KEY, LANGUAGE)
    
    logger.info("Generating article...")
    article = generator.generate_article(
        news_items,
        title="AI 뉴스 자동 생성 리포트"
    )
    
    # Save article
    filepath = save_article(article)
    
    logger.info("AI News Automation completed successfully!")
    logger.info(f"Generated article available at: {filepath}")
    
    # Print preview
    print("\n" + "="*80)
    print("ARTICLE PREVIEW")
    print("="*80)
    print(article[:500] + "..." if len(article) > 500 else article)
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        sys.exit(1)
