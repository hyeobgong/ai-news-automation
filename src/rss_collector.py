import feedparser
import urllib.parse

def collect_news(query, hl='ko', gl='KR', ceid='KR:ko'):
    """
    Google News RSS에 쿼리를 전송하여 뉴스를 수집합니다.
    - query: 검색어
    - hl: 호스트 언어 (예: ko, en-US)
    - gl: 지리적 위치 (예: KR, US)
    - ceid: 콘텐츠 에디션 ID (예: KR:ko, US:en)
    """
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl={hl}&gl={gl}&ceid={ceid}"
    
    print(f"Fetching news for: {query} (Region: {gl}, Lang: {hl})")
    print(f"RSS URL: {rss_url}\n")
    
    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(f"RSS parsing error: {e}")
        return []
    
    if not feed.entries:
        print("No news found.")
        return []

    news_list = []
    print(f"Found {len(feed.entries)} articles. Extracting top 20...\n")
    
    # 상위 20개 기사만 수집 (테스트 목적)
    for i, entry in enumerate(feed.entries[:20]):
        news_item = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary if 'summary' in entry else ''
        }
        news_list.append(news_item)
        
    return news_list

if __name__ == "__main__":
    # Test with "Generative AI"
    collect_news("생성형 AI")
