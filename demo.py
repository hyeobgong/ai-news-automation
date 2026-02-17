"""
Demo script with mock data to demonstrate the AI news automation
"""
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from content_generator import ContentGenerator


def create_mock_news_data():
    """Create mock news data for demonstration"""
    return [
        {
            'title': 'OpenAI, GPT-4 Turbo 모델 공식 출시',
            'link': 'https://example.com/news1',
            'published': '2026-02-17T10:00:00',
            'summary': 'OpenAI가 최신 GPT-4 Turbo 모델을 공식 출시했습니다. 이 모델은 이전 버전보다 빠른 속도와 향상된 성능을 제공합니다.',
            'source': 'AI Times'
        },
        {
            'title': '구글, 차세대 AI 칩 개발 발표',
            'link': 'https://example.com/news2',
            'published': '2026-02-17T09:30:00',
            'summary': '구글이 AI 워크로드에 최적화된 차세대 TPU 칩을 발표했습니다. 새로운 칩은 에너지 효율성이 크게 개선되었습니다.',
            'source': 'Tech News'
        },
        {
            'title': '삼성전자, AI 반도체 신제품 라인업 공개',
            'link': 'https://example.com/news3',
            'published': '2026-02-16T15:00:00',
            'summary': '삼성전자가 AI와 머신러닝 작업에 특화된 새로운 반도체 제품군을 공개했습니다.',
            'source': 'IT Daily'
        },
        {
            'title': '마이크로소프트, 코파일럿 기능 대폭 업데이트',
            'link': 'https://example.com/news4',
            'published': '2026-02-16T14:00:00',
            'summary': '마이크로소프트가 GitHub 코파일럿에 새로운 AI 기능을 추가하며 개발자 생산성 향상을 목표로 합니다.',
            'source': 'Developer News'
        },
        {
            'title': 'AI 윤리 가이드라인 국제 표준 제정',
            'link': 'https://example.com/news5',
            'published': '2026-02-15T10:00:00',
            'summary': 'UN 주도로 AI 윤리 및 안전성에 관한 국제 표준 가이드라인이 제정되었습니다.',
            'source': 'Global Tech'
        }
    ]


def main():
    """Run demo with mock data"""
    print("="*80)
    print("AI News Automation - Demo")
    print("="*80 + "\n")
    
    # Create mock news data
    print("Creating mock news data...")
    news_items = create_mock_news_data()
    print(f"✓ Created {len(news_items)} mock news items\n")
    
    # Initialize content generator (without API key for demo)
    print("Initializing content generator...")
    generator = ContentGenerator(api_key='', language='ko')
    print("✓ Content generator initialized (basic mode)\n")
    
    # Generate article
    print("Generating article...")
    article = generator.generate_article(
        news_items,
        title="AI 뉴스 자동 생성 리포트 (데모)"
    )
    print(f"✓ Article generated ({len(article)} characters)\n")
    
    # Save article
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"demo_ai_news_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article)
    
    print(f"✓ Article saved to: {filepath}\n")
    
    # Display preview
    print("="*80)
    print("ARTICLE PREVIEW")
    print("="*80)
    print(article)
    print("="*80 + "\n")
    
    print("Demo completed successfully! ✓")
    print(f"\nYou can find the full article at: {filepath}")


if __name__ == "__main__":
    main()
