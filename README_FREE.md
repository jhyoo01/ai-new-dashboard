# 📊 글비 빅테크 리포트 - 완전 무료 버전! 🎉

<div align="center">

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success?style=for-the-badge&logo=github)](https://jhyoo01.github.io/bigtech-report-dashboard/)
[![Auto Update](https://img.shields.io/badge/Auto%20Update-Daily%209AM-blue?style=for-the-badge)](https://github.com/jhyoo01/bigtech-report-dashboard/actions)
[![100% Free](https://img.shields.io/badge/Cost-$0-green?style=for-the-badge)](README.md)

**Google, Meta, YouTube, TikTok, PayPal, Stripe, Microsoft, Amazon**

매일 오전 9시 자동 업데이트 | 완전 무료 | API 키 불필요

</div>

---

## ✨ 주요 기능

- 🆓 **완전 무료** - API 키, 비용 전혀 없음!
- ⏰ **매일 오전 9시 자동 업데이트** - GitHub Actions
- 📅 **최근 14일 뉴스만 표시**
- 📰 **기업당 50-100개 뉴스 수집**
- 🔄 **자동 중복 제거**
- ⭐ **TechCrunch/The Verge 우선 노출**
- 🔝 **최신순 정렬**
- 🇰🇷 **한글 키워드 번역**

---

## 🚀 5분 만에 설정하기

### 1단계: 저장소 생성

1. GitHub에서 새 저장소 생성
2. 이름: `bigtech-report-dashboard`
3. Public으로 설정

### 2단계: 파일 업로드

다음 파일 구조로 업로드:

```
bigtech-report-dashboard/
├── .github/
│   └── workflows/
│       ├── update-news.yml    ← 자동 업데이트
│       └── deploy.yml         ← GitHub Pages 배포
├── scripts/
│   └── update_news.py         ← 뉴스 크롤러
├── index.html                 ← 대시보드
├── bigtech_data_latest.json   ← 뉴스 데이터
└── README.md
```

### 3단계: GitHub Pages 활성화

1. Settings → Pages
2. Source: **GitHub Actions** 선택
3. 완료!

### 4단계: 첫 실행

1. Actions 탭 이동
2. "Daily BigTech News Update" 선택
3. "Run workflow" 클릭
4. 1-2분 대기
5. 사이트 접속!

---

## 🎯 수집 대상

<table>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/Google-4285F4?style=for-the-badge&logo=google&logoColor=white"/><br>
<b>Google</b>
</td>
<td align="center">
<img src="https://img.shields.io/badge/Meta-0668E1?style=for-the-badge&logo=meta&logoColor=white"/><br>
<b>Meta</b>
</td>
<td align="center">
<img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"/><br>
<b>YouTube</b>
</td>
<td align="center">
<img src="https://img.shields.io/badge/TikTok-000000?style=for-the-badge&logo=tiktok&logoColor=white"/><br>
<b>TikTok</b>
</td>
</tr>
<tr>
<td align="center">
<img src="https://img.shields.io/badge/PayPal-003087?style=for-the-badge&logo=paypal&logoColor=white"/><br>
<b>PayPal</b>
</td>
<td align="center">
<img src="https://img.shields.io/badge/Stripe-008CDD?style=for-the-badge&logo=stripe&logoColor=white"/><br>
<b>Stripe</b>
</td>
<td align="center">
<img src="https://img.shields.io/badge/Microsoft-00A4EF?style=for-the-badge&logo=microsoft&logoColor=white"/><br>
<b>Microsoft</b>
</td>
<td align="center">
<img src="https://img.shields.io/badge/Amazon-FF9900?style=for-the-badge&logo=amazon&logoColor=white"/><br>
<b>Amazon</b>
</td>
</tr>
</table>

---

## 🔧 작동 원리

### 뉴스 수집

```
Google News RSS 피드 활용
    ↓
각 기업별 최대 100개 뉴스 수집
    ↓
14일 이내 뉴스만 필터링
    ↓
중복 제거 (제목 해시)
    ↓
TechCrunch/The Verge 우선 정렬
    ↓
최신순 정렬
    ↓
한글 키워드 번역
    ↓
JSON 파일 생성
```

### 자동 업데이트

```yaml
schedule:
  - cron: '0 0 * * *'  # 매일 UTC 0시 = KST 9시
```

---

## 📂 파일 설명

### `.github/workflows/update-news.yml`
```yaml
# 매일 오전 9시 자동 실행
# Python 크롤러 실행
# 변경사항 자동 커밋 & 푸시
```

### `scripts/update_news.py`
```python
# Google News RSS 크롤링
# 중복 제거, 필터링, 정렬
# JSON 파일 생성
```

### `index.html`
```html
<!-- 다크 테마 대시보드 -->
<!-- 한글 번역 지원 -->
<!-- 반응형 디자인 -->
```

---

## 🎨 커스터마이징

### 수집 기업 추가

`scripts/update_news.py` 수정:

```python
COMPANIES = {
    'Google': ['Google', 'Alphabet'],
    'Tesla': ['Tesla', 'Elon Musk'],  # 추가!
    # ...
}
```

### 뉴스 개수 조절

```python
# 각 기업당 최대 30개로 제한
articles = self.collect_news_for_company(company, keywords, target_count=30)
```

### 실행 시간 변경

```yaml
# 매일 오후 6시 (UTC 9시 = KST 18시)
schedule:
  - cron: '0 9 * * *'
```

---

## 💡 왜 무료인가요?

### AI 대시보드 방식 그대로!

- ✅ Google News RSS (무료 공개 API)
- ✅ GitHub Actions (월 2,000분 무료)
- ✅ GitHub Pages (무료 호스팅)
- ✅ Python 크롤링 (오픈소스)

### API 키 불필요

- ❌ Anthropic API 필요 없음
- ❌ OpenAI API 필요 없음
- ❌ 유료 뉴스 API 필요 없음

---

## 📊 비교표

| 항목 | AI 대시보드 | 빅테크 대시보드 |
|------|-------------|----------------|
| 비용 | **$0** | **$0** |
| 자동 업데이트 | ✅ | ✅ |
| API 키 | 불필요 | 불필요 |
| 뉴스 수집 | Google RSS | Google RSS |
| 한글 지원 | ❌ | ✅ |
| 수집 기업 | AI 관련 | 8개 빅테크 |

---

## 🔍 FAQ

### Q: 정말 완전 무료인가요?
**A:** 네! GitHub Actions와 Google News RSS는 완전 무료입니다.

### Q: API 키가 필요 없나요?
**A:** 전혀 필요 없습니다!

### Q: 뉴스 품질은 어떤가요?
**A:** Google News에서 수집하므로 신뢰할 수 있습니다.

### Q: 한글 번역은 자동인가요?
**A:** 주요 키워드만 한글로 표시됩니다 (예: AI(인공지능), acquisition(인수))

### Q: 수동 업데이트도 가능한가요?
**A:** 네! Actions 탭에서 "Run workflow" 클릭하면 됩니다.

---

## 🐛 문제 해결

### 뉴스가 업데이트되지 않음

1. Actions 탭 확인
2. 워크플로우 로그 확인
3. 수동으로 재실행

### 중복 뉴스가 보임

`scripts/update_news.py`의 해시 함수 조정:
```python
normalized = re.sub(r'[^\w\s]', '', title.lower()[:100])  # 100자로 증가
```

---

## 📈 로드맵

- [ ] 더 많은 뉴스 소스 추가
- [ ] 전문 한글 번역 API 통합
- [ ] 뉴스 카테고리 필터 개선
- [ ] 모바일 앱 버전
- [ ] 이메일 알림 기능

---

## 🤝 기여

개선 사항이 있으시면 PR 환영합니다!

---

## 📝 라이선스

MIT License

---

<div align="center">

**Made with ❤️ for BigTech News Monitoring**

⭐ 이 프로젝트가 유용하다면 Star를 눌러주세요!

[Live Demo](https://jhyoo01.github.io/bigtech-report-dashboard/) | [Report Issue](https://github.com/jhyoo01/bigtech-report-dashboard/issues)

</div>
