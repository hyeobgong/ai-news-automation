import os
import sys
from datetime import datetime

print("DEBUG: Script Start")

# src 폴더를 파이썬 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rss_collector import collect_news
from news_processor import process_news
from report_generator import generate_markdown_report

def main():
    print(f"\n======== [AI 뉴스 자동화 시스템 시작] ========")
    print(f"시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. 뉴스 수집 (Collecting)
    print(">>> 1. 최신 AI 뉴스 수집 중...")
    try:
        raw_news = []

        # 1-1. 미국(영어) 뉴스 수집 (우선순위를 높이기 위해 먼저 수집)
        us_keywords = ["Generative AI", "Artificial Intelligence"]
        us_news_list = []
        for keyword in us_keywords:
            print(f"  🔍 [US] 검색어 '{keyword}' 수집 중...")
            news = collect_news(keyword, hl='en', gl='US', ceid='US:en')
            us_news_list.extend(news)
            
        # 1-2. 한국 뉴스 수집
        kr_keywords = ["생성형 AI", "인공지능 트렌드"]
        kr_news_list = []
        for keyword in kr_keywords:
            print(f"  🔍 [KR] 검색어 '{keyword}' 수집 중...")
            news = collect_news(keyword, hl='ko', gl='KR', ceid='KR:ko')
            kr_news_list.extend(news)

        # 1-3. 뉴스 섞기 (미국2 : 한국1 비율)
        # 앞에서부터 자를 때 골고루 들어가도록 배치
        max_idx = max(len(us_news_list), len(kr_news_list))
        
        for i in range(max_idx):
            # 미국 뉴스 2개 추가
            if i*2 < len(us_news_list):
                 raw_news.append(us_news_list[i*2])
            if i*2+1 < len(us_news_list):
                 raw_news.append(us_news_list[i*2+1])
            
            # 한국 뉴스 1개 추가
            if i < len(kr_news_list):
                 raw_news.append(kr_news_list[i])
            
        if not raw_news:
            print("❌ 수집된 뉴스가 없습니다. 프로그램을 종료합니다.")
            return
        print(f"✅ 총 {len(raw_news)}건의 뉴스 수집 완료.\n")
    except Exception as e:
        print(f"❌ 뉴스 수집 중 오류 발생: {e}")
        return

    # 2. 뉴스 처리 및 분석 (Processing & Analyzing)
    print(">>> 2. 뉴스 중복 제거 및 AI 분석 시작...")
    try:
        processed_news = process_news(raw_news)
        if not processed_news:
            print("⚠️ 처리된 데이터가 없습니다.")
            return
        print(f"✅ 분석 완료: {len(processed_news)}건의 중요 뉴스 선별됨.\n")
    except Exception as e:
        print(f"❌ 뉴스 처리 중 오류 발생: {e}")
        return

    # 3. 리포트 생성 (Reporting)
    print(">>> 3. 최종 보고서 생성 중...")
    try:
        report_file = generate_markdown_report(processed_news)
        if report_file:
            print(f"🎉 모든 작업이 성공적으로 완료되었습니다!")
            print(f"📄 결과 파일 확인: {os.path.abspath(report_file)}")
        else:
            print("⚠️ 보고서 파일 생성 실패.")
    except Exception as e:
        print(f"❌ 보고서 생성 중 오류 발생: {e}")

    print("\n======== [시스템 종료] ========")

if __name__ == "__main__":
    main()
