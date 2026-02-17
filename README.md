# AI News Automation (AI 뉴스 자동생성)

AI 관련 뉴스를 자동으로 수집하고 요약하는 프로젝트입니다.

## 기능 (Features)

- 📰 **자동 뉴스 수집**: RSS 피드에서 최신 AI 뉴스를 자동으로 수집
- 🤖 **AI 요약**: OpenAI API를 사용하여 뉴스를 지능적으로 요약
- 📝 **콘텐츠 생성**: 수집된 뉴스를 마크다운 형식의 리포트로 자동 생성
- ⏰ **스케줄 자동화**: GitHub Actions를 통한 매일 자동 실행
- 🌏 **한국어 지원**: 한국어 AI 뉴스 소스 및 요약 지원

## 프로젝트 구조

```
ai-news-automation/
├── src/
│   ├── config.py              # 설정 및 환경변수
│   ├── news_fetcher.py        # 뉴스 수집 모듈
│   └── content_generator.py   # AI 콘텐츠 생성 모듈
├── output/                    # 생성된 뉴스 리포트
├── .github/workflows/         # GitHub Actions 워크플로우
├── main.py                    # 메인 실행 스크립트
├── requirements.txt           # Python 의존성
├── .env.example              # 환경변수 예시
└── README.md                  # 프로젝트 문서
```

## 설치 방법 (Installation)

1. **저장소 클론**
```bash
git clone https://github.com/hyeobgong/ai-news-automation.git
cd ai-news-automation
```

2. **Python 가상환경 생성 (권장)**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **환경변수 설정**
```bash
cp .env.example .env
# .env 파일을 편집하여 API 키 입력
```

`.env` 파일에 다음 정보를 입력하세요:
```
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_news_api_key_here  # 선택사항
MAX_NEWS_ITEMS=10
LANGUAGE=ko
```

## 사용 방법 (Usage)

### 로컬 실행

```bash
python main.py
```

실행 후 `output/` 디렉토리에 생성된 마크다운 파일을 확인할 수 있습니다.

### GitHub Actions 자동화

1. GitHub 저장소의 Settings > Secrets and variables > Actions로 이동
2. 다음 Secret을 추가:
   - `OPENAI_API_KEY`: OpenAI API 키
   - `NEWS_API_KEY`: News API 키 (선택사항)

3. 워크플로우는 매일 오전 9시(KST)에 자동 실행됩니다.
4. 수동 실행: Actions 탭에서 "AI News Automation" 워크플로우를 선택하고 "Run workflow" 클릭

## 설정 커스터마이징

### RSS 피드 추가

`src/config.py` 파일의 `RSS_FEEDS` 리스트를 수정하여 원하는 RSS 피드를 추가할 수 있습니다:

```python
RSS_FEEDS = [
    'https://www.aitimes.com/rss/allArticle.xml',
    'https://www.techneedle.com/rss/allArticle.xml',
    # 추가 RSS 피드 URL
]
```

### 뉴스 항목 개수 조정

`.env` 파일의 `MAX_NEWS_ITEMS` 값을 수정하여 수집할 뉴스 개수를 조절할 수 있습니다.

## 요구사항 (Requirements)

- Python 3.8 이상
- OpenAI API 키 (AI 요약 기능을 사용하려면 필요)
- 인터넷 연결

## 의존성 (Dependencies)

- `feedparser`: RSS 피드 파싱
- `requests`: HTTP 요청
- `beautifulsoup4`: HTML 파싱
- `openai`: OpenAI API 클라이언트
- `python-dotenv`: 환경변수 관리

## 라이선스 (License)

MIT License

## 기여 (Contributing)

이슈 및 Pull Request를 환영합니다!

## 문의 (Contact)

프로젝트와 관련된 질문이나 제안사항이 있으시면 이슈를 생성해주세요.

---

**참고**: OpenAI API 사용 시 비용이 발생할 수 있습니다. API 키 설정 없이도 기본적인 뉴스 수집 기능은 사용할 수 있습니다.