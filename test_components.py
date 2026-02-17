"""
Simple test script to verify the AI news automation components
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from news_fetcher import NewsFetcher
from content_generator import ContentGenerator


def test_news_fetcher():
    """Test the news fetcher module"""
    print("Testing News Fetcher...")
    
    # Test with sample RSS feeds
    test_feeds = [
        'https://www.aitimes.com/rss/allArticle.xml',
    ]
    
    fetcher = NewsFetcher(test_feeds, max_items=3)
    news_items = fetcher.fetch_news()
    
    print(f"✓ Fetched {len(news_items)} news items")
    
    if news_items:
        print(f"✓ Sample news item: {news_items[0]['title'][:50]}...")
    
    return news_items


def test_content_generator(news_items):
    """Test the content generator module"""
    print("\nTesting Content Generator...")
    
    # Test without API key (basic mode)
    generator = ContentGenerator(api_key='', language='ko')
    
    # Test basic summary
    summary = generator._generate_basic_summary(news_items)
    print(f"✓ Generated basic summary ({len(summary)} characters)")
    
    # Test basic article
    article = generator._generate_basic_article(news_items, "Test Article")
    print(f"✓ Generated basic article ({len(article)} characters)")
    
    return article


def main():
    """Run all tests"""
    print("="*60)
    print("AI News Automation - Component Tests")
    print("="*60 + "\n")
    
    try:
        # Test 1: News Fetcher
        news_items = test_news_fetcher()
        
        if not news_items:
            print("\n⚠ No news items fetched. Tests incomplete.")
            print("This might be due to network issues or RSS feed availability.")
            return
        
        # Test 2: Content Generator
        article = test_content_generator(news_items[:3])
        
        print("\n" + "="*60)
        print("All tests completed successfully! ✓")
        print("="*60)
        
        print("\nSample Article Preview:")
        print("-"*60)
        print(article[:300] + "..." if len(article) > 300 else article)
        print("-"*60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
