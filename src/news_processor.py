import os
import json
import re
import time
from google import genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Gemini 설정 (google-genai v1.0 이상)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# 최신 google-genai 패키지 사용 방식
client = genai.Client(api_key=GEMINI_API_KEY)

def deduplicate_news(news_list, similarity_threshold=0.6):
    """
    뉴스 리스트에서 중복/유사 기사를 제거합니다.
    임계값을 0.6으로 낮추어 더 많은 중복을 잡도록 조정했습니다.
    """
    if not news_list:
        return []
    
    # 1. 텍스트 추출 (제목만 사용)
    texts = [item['title'] for item in news_list]
    
    # 2. TF-IDF 벡터화
    # 한글 처리는 복잡하므로 간단하게 공백 기준으로 벡터화
    # analyzer='char_wb', ngram_range=(2,3) -> 철자가 비슷하면 중복으로 인식
    vectorizer = TfidfVectorizer(min_df=1, analyzer='char_wb', ngram_range=(2,3))
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # 3. 코사인 유사도 계산
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    # 4. 중복 제거 중...
    unique_news = []
    visited = [False] * len(news_list)
    
    # 디버깅: 유사도 행렬 출력
    # print("Similarity Matrix:\n", similarity_matrix)
    
    for i in range(len(news_list)):
        if visited[i]:
            continue
        
        # 현재 기사를 대표 기사로 선정
        representative = news_list[i]
        related_articles = []
        
        visited[i] = True
        
        for j in range(i + 1, len(news_list)):
            if not visited[j]:
                sim = similarity_matrix[i][j]
                if sim >= similarity_threshold:
                    visited[j] = True
                    related_articles.append(news_list[j])
                    print(f"  [중복제거] '{news_list[i]['title']}' 유사 기사 제거: '{news_list[j]['title']}' ({sim:.2f})")
        
        # 묶인 기사 정보 저장
        representative['related_links'] = [r['link'] for r in related_articles]
        unique_news.append(representative)
        
    print(f"📉 중복 제거 완료: {len(news_list)} -> {len(unique_news)} 건 (유사도 기준: {similarity_threshold})")
    return unique_news

def analyze_news_with_gemini(news_item):
    """
    Gemini를 사용하여 뉴스를 분석하고 요약합니다.
    """
    prompt = f"""
    당신은 AI 뉴스 전문 분석가입니다. 아래 뉴스 기사를 분석하여 JSON 형식으로 응답해주세요.
    
    [뉴스 정보]
    제목: {news_item['title']}
    링크: {news_item['link']}
    발행일: {news_item['published']}
    
    [요청 사항]
    1. **카테고리 분류**: 다음 두 그룹 중 하나를 선택하고, 세부 주제를 명시하세요.
       - 그룹1 (기술 중심): LLM 모델, 서비스/에이전트, 하드웨어/피지컬AI 등
       - 그룹2 (사회/경제 중심): 비즈니스/투자, 규제/윤리 등
       
    2. **제목 번역**: 기사의 제목을 자연스러운 한국어로 번역하세요.

    3. **3줄 요약**: 기사의 핵심 내용을 한국어 3문장으로 요약하세요.
    (반드시 JSON 형식만 출력해야 합니다. 마크다운이나 코드블록 없이 순수 JSON.)
    
    [출력 예시]
    {{
        "title_ko": "번역된 한국어 기사 제목",
        "category_group": "그룹1 (기술 중심)",
        "topic": "LLM 모델",
        "summary": ["첫번째 문장입니다.", "두번째 문장입니다.", "세번째 문장입니다."],
        "importance": 5
    }}
    """
    
    # 재시도 로직 추가 (최대 3회, 지수 백오프)
    max_retries = 3
    retry_delay = 10
    
    for attempt in range(max_retries):
        try:
            print(f"  - Gemini 요청 중... ({news_item['title'][:15]}...) [시도 {attempt+1}/{max_retries}]")
            
            # 모델: 'gemini-2.0-flash-lite' 사용
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite", 
                contents=prompt,
            )
            
            text = response.text
            # 코드 블록(```json) 제거
            text = re.sub(r"```json|```", "", text).strip()
            analysis = json.loads(text)
            
            # 성공 시 1초 대기 후 반환 (속도를 빠르게 조정)
            time.sleep(1) 
            return analysis
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"    ⚠️ 할당량 초과(429). {retry_delay}초 대기 후 재시도합니다...")
                time.sleep(retry_delay)
                retry_delay *= 2  # 대기 시간 2배로 증가 (Exponential Backoff)
            else:
                print(f"    ⚠️ 분석 오류 발생: {e}")
                break  # 429가 아니면 재시도하지 않고 중단
    
    # 모든 재시도 실패 시 더미 데이터 반환
    print("  ❌ 모든 재시도 실패. 더미 데이터로 대체합니다.")
    return {
        "category_group": "미분류 (분석 실패)",
        "topic": "API 오류",
        "summary": ["AI 분석에 실패하여 원문 링크를 확인해주세요.", "API 할당량 초과 또는 네트워크 문제입니다.", "잠시 후 다시 시도해주세요."],
        "importance": 1
    }

def process_news(news_list):
    """
    전체 뉴스 처리 파이프라인
    """
    # 1. 중복 제거
    unique_news = deduplicate_news(news_list)
    
    processed_news = []
    
    print("\n🧠 Gemini AI 분석 시작...")
    
    # 상위 20개 뉴스 분석 (사용자 요청 반영)
    processed_count = 0
    max_process = 20
    
    total_to_process = min(len(unique_news), max_process)
    print(f"👉 총 {total_to_process}개의 주요 뉴스를 분석합니다.\n")

    for i, news in enumerate(unique_news): 
        if processed_count >= max_process:
            break
            
        print(f"[{processed_count + 1}/{total_to_process}] 분석 중: {news['title'][:30]}...")
        analysis = analyze_news_with_gemini(news)
        
        if analysis:
            # 원본 뉴스 객체에 분석 결과 병합
            news.update(analysis)
            
            # 한국어 제목이 있으면 적용
            if 'title_ko' in analysis:
                 news['title'] = analysis['title_ko']

            processed_news.append(news)
            print(f"  ✅ 완료! -> {news['title']}")
            processed_count += 1
            
    return processed_news

if __name__ == "__main__":
    # 테스트 데이터 (가상)
    test_data = [
        {'title': 'OpenAI, 새로운 GPT-5 모델 출시 임박', 'link': 'http://example.com/1', 'published': '2026-02-18'},
        {'title': 'OpenAI GPT-5 출시 예정, 성능 대폭 향상', 'link': 'http://example.com/2', 'published': '2026-02-18'}, # 중복
        {'title': '구글 제미나이, 헬스케어 분야 진출', 'link': 'http://example.com/3', 'published': '2026-02-17'},
        {'title': 'AI 규제 법안 국회 통과, 기업들 비상', 'link': 'http://example.com/4', 'published': '2026-02-16'},
    ]
    
    print("--- 테스트 시작 ---")
    results = process_news(test_data)
    
    print("\n--- 최종 결과 (JSON) ---")
    print(json.dumps(results, indent=2, ensure_ascii=False))
