"""
AI Content Generator Module
Uses OpenAI API to generate summaries and content from news
"""
import logging
from typing import List, Dict, Optional
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generates AI-powered content summaries"""
    
    def __init__(self, api_key: str, language: str = 'ko'):
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.language = language
    
    def generate_summary(self, news_items: List[Dict]) -> str:
        """Generate a comprehensive summary of multiple news items"""
        if not self.client:
            logger.warning("OpenAI API key not configured, returning basic summary")
            return self._generate_basic_summary(news_items)
        
        try:
            # Prepare news content for summarization
            news_content = "\n\n".join([
                f"제목: {item['title']}\n요약: {item['summary']}\n출처: {item['source']}"
                for item in news_items
            ])
            
            prompt = f"""다음은 최근 AI 관련 뉴스들입니다. 이 뉴스들을 종합하여 한국어로 간결하고 이해하기 쉬운 요약을 작성해주세요.

{news_content}

주요 트렌드와 중요한 내용을 중심으로 요약해주세요."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 AI 뉴스를 전문적으로 요약하는 기자입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content
            logger.info("Successfully generated AI summary")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating AI summary: {str(e)}")
            return self._generate_basic_summary(news_items)
    
    def _generate_basic_summary(self, news_items: List[Dict]) -> str:
        """Generate a basic summary without AI"""
        summary = "# AI 뉴스 요약\n\n"
        for i, item in enumerate(news_items, 1):
            summary += f"{i}. **{item['title']}**\n"
            summary += f"   - 출처: {item['source']}\n"
            summary += f"   - 링크: {item['link']}\n"
            if item.get('summary'):
                summary += f"   - 요약: {item['summary'][:100]}...\n"
            summary += "\n"
        return summary
    
    def generate_article(self, news_items: List[Dict], title: str = "AI 뉴스 모음") -> str:
        """Generate a complete article from news items"""
        if not self.client:
            logger.warning("OpenAI API key not configured, returning basic article")
            return self._generate_basic_article(news_items, title)
        
        try:
            summary = self.generate_summary(news_items)
            
            article = f"# {title}\n\n"
            article += f"생성일시: {self._get_current_time()}\n\n"
            article += "## 주요 내용\n\n"
            article += summary + "\n\n"
            article += "## 개별 뉴스 항목\n\n"
            article += self._format_news_items(news_items)
            
            return article
            
        except Exception as e:
            logger.error(f"Error generating article: {str(e)}")
            return self._generate_basic_article(news_items, title)
    
    def _generate_basic_article(self, news_items: List[Dict], title: str) -> str:
        """Generate a basic article without AI enhancement"""
        article = f"# {title}\n\n"
        article += f"생성일시: {self._get_current_time()}\n\n"
        article += "## 뉴스 목록\n\n"
        article += self._format_news_items(news_items)
        return article
    
    def _format_news_items(self, news_items: List[Dict]) -> str:
        """Format news items for display"""
        formatted = ""
        for i, item in enumerate(news_items, 1):
            formatted += f"### {i}. {item['title']}\n\n"
            formatted += f"**출처:** {item['source']}  \n"
            formatted += f"**링크:** [{item['link']}]({item['link']})  \n"
            if item.get('published'):
                formatted += f"**발행일:** {item['published']}  \n"
            if item.get('summary'):
                formatted += f"\n{item['summary']}\n"
            formatted += "\n---\n\n"
        return formatted
    
    @staticmethod
    def _get_current_time() -> str:
        """Get current time as formatted string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
