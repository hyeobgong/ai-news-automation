import os
from datetime import datetime

def generate_markdown_report(news_data):
    """
    처리된 뉴스 데이터를 마크다운 보고서로 생성하고 저장합니다.
    """
    if not news_data:
        print("📭 처리된 뉴스가 없습니다.")
        return None

    today = datetime.now().strftime("%Y-%m-%d")
    report_content = f"# 🗞️ AI 뉴스 일일 브리핑 ({today})\n\n"
    report_content += "본 보고서는 AI 자동화 시스템에 의해 수집 및 요약되었습니다.\n\n"
    report_content += "---\n\n"

    # 카테고리별로 그룹화 (선택 사항, 지금은 리스트 순서대로 출력)
    # 중요도가 높은 순으로 정렬
    sorted_news = sorted(news_data, key=lambda x: x.get('importance', 0), reverse=True)

    for idx, news in enumerate(sorted_news, 1):
        title = news.get('title', '제목 없음')
        link = news.get('link', '#')
        category = news.get('category_group', '기타')
        topic = news.get('topic', '')
        summary = news.get('summary', [])
        importance = news.get('importance', 1)
        
        # 중요도 아이콘 표시
        star_icon = "⭐" * importance
        
        report_content += f"## {idx}. {title}\n"
        report_content += f"**분류**: {category} > {topic} | **중요도**: {star_icon}\n\n"
        
        report_content += "**요약**:\n"
        if isinstance(summary, list):
            for line in summary:
                report_content += f"- {line}\n"
        else:
            report_content += f"- {summary}\n"
            
        report_content += f"\n[🔗 원문 기사 보러가기]({link})\n\n"
        report_content += "---\n\n"

    # reports 폴더가 없으면 생성
    os.makedirs("reports", exist_ok=True)
    
    # 시간 표시 추가: 14시_30분
    current_time_str = datetime.now().strftime("%H시%M분")
    filename = f"reports/{today}_{current_time_str}_AI_News_Report.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"✅ 보고서 생성 완료: {filename}")
    return filename
