#!/usr/bin/env python3
"""
빅테크 뉴스 자동 수집 스크립트 (완전 무료)
Google News RSS를 활용한 뉴스 크롤링
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import hashlib
import re
from urllib.parse import quote
import time

class BigTechNewsCrawler:
    """무료 빅테크 뉴스 크롤러"""
    
    COMPANIES = {
        'Google': ['Google', 'Alphabet'],
        'Meta': ['Meta', 'Facebook', 'Instagram'],
        'YouTube': ['YouTube'],
        'TikTok': ['TikTok', 'ByteDance'],
        'PayPal': ['PayPal'],
        'Stripe': ['Stripe'],
        'Microsoft': ['Microsoft'],
        'Amazon': ['Amazon', 'AWS']
    }
    
    PRIORITY_SOURCES = ['techcrunch.com', 'theverge.com', 'TechCrunch', 'The Verge']
    
    def __init__(self):
        self.news_data = {}
        self.seen_titles = set()
        self.cutoff_date = datetime.now() - timedelta(days=14)
        
        for company in self.COMPANIES.keys():
            self.news_data[company] = []
    
    def generate_hash(self, title):
        """제목 해시 생성 (중복 제거)"""
        normalized = re.sub(r'[^\w\s]', '', title.lower()[:80])
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def is_duplicate(self, title):
        """중복 체크"""
        title_hash = self.generate_hash(title)
        if title_hash in self.seen_titles:
            return True
        self.seen_titles.add(title_hash)
        return False
    
    def extract_domain(self, url):
        """도메인 추출"""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            return domain.replace('www.', '')
        except:
            return 'Unknown'
    
    def calculate_importance(self, title, source, is_recent):
        """중요도 점수 계산"""
        score = 50
        
        # 우선 출처
        if any(priority in source for priority in self.PRIORITY_SOURCES):
            score += 25
        
        # 키워드 가중치
        title_lower = title.lower()
        high_priority_words = ['billion', 'acquisition', 'launch', 'announces', 'breakthrough', 'major']
        score += sum(10 for word in high_priority_words if word in title_lower)
        
        # 최근성
        if is_recent:
            score += 15
        
        return min(score, 100)
    
    def categorize_article(self, title, snippet):
        """카테고리 자동 분류"""
        text = f"{title} {snippet}".lower()
        
        if any(word in text for word in ['launch', 'release', 'unveil', 'announce']):
            return 'Product Launch'
        elif any(word in text for word in ['revenue', 'earnings', 'profit', 'stock']):
            return 'Financial Results'
        elif any(word in text for word in ['regulation', 'law', 'lawsuit', 'fine', 'court']):
            return 'Regulation & Policy'
        elif any(word in text for word in ['ai', 'artificial intelligence', 'technology', 'innovation']):
            return 'Technology Innovation'
        elif any(word in text for word in ['compete', 'rival', 'versus', 'market share']):
            return 'Competition'
        elif any(word in text for word in ['ceo', 'executive', 'appoint', 'resign']):
            return 'Leadership & Strategy'
        else:
            return 'Market Trends'
    
    def translate_to_korean(self, text):
        """간단한 한글 번역 (키워드 기반)"""
        translations = {
            'announces': '발표',
            'launch': '출시',
            'acquires': '인수',
            'acquisition': '인수',
            'reports': '보고',
            'invests': '투자',
            'investment': '투자',
            'expands': '확장',
            'introduces': '도입',
            'unveils': '공개',
            'partners': '파트너십',
            'partnership': '파트너십 체결',
            'billion': '십억',
            'million': '백만',
            'AI': '인공지능',
            'artificial intelligence': '인공지능',
            'data center': '데이터센터',
            'cloud': '클라우드',
            'revenue': '매출',
            'earnings': '실적',
            'profit': '이익',
            'stock': '주가',
            'CEO': 'CEO',
            'deal': '거래',
            'agreement': '계약'
        }
        
        result = text
        for eng, kor in translations.items():
            result = re.sub(r'\b' + re.escape(eng) + r'\b', f'{eng}({kor})', result, flags=re.IGNORECASE)
        
        return result
    
    def search_google_news(self, query, max_results=20):
        """Google News 검색"""
        try:
            # Google News RSS 피드 사용
            encoded_query = quote(query)
            url = f'https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en'
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')[:max_results]
            
            articles = []
            for item in items:
                try:
                    title = item.title.text if item.title else ''
                    link = item.link.text if item.link else ''
                    pub_date = item.pubDate.text if item.pubDate else ''
                    description = item.description.text if item.description else ''
                    
                    # 날짜 파싱
                    try:
                        pub_datetime = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
                        date_str = pub_datetime.strftime('%Y-%m-%d')
                        is_recent = pub_datetime >= self.cutoff_date
                    except:
                        date_str = datetime.now().strftime('%Y-%m-%d')
                        is_recent = True
                    
                    # 14일 필터
                    if not is_recent:
                        continue
                    
                    # 출처 추출
                    source = self.extract_domain(link)
                    
                    articles.append({
                        'title': title,
                        'url': link,
                        'snippet': description,
                        'source': source,
                        'published_date': date_str,
                        'is_recent': is_recent
                    })
                    
                except Exception as e:
                    print(f"  ⚠️  Item parsing error: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            print(f"  ❌ Search error for '{query}': {e}")
            return []
    
    def collect_news_for_company(self, company, keywords, target_count=50):
        """특정 기업의 뉴스 수집"""
        print(f"\n🔍 Collecting news for {company}...")
        
        all_articles = []
        
        # 각 키워드로 검색
        for keyword in keywords[:2]:  # 주요 키워드 2개만 사용
            search_query = f'{keyword} news'
            articles = self.search_google_news(search_query, max_results=30)
            
            for article in articles:
                # 중복 체크
                if self.is_duplicate(article['title']):
                    continue
                
                # 회사명 관련성 체크
                title_lower = article['title'].lower()
                if not any(kw.lower() in title_lower for kw in keywords):
                    continue
                
                # 카테고리 분류
                article['category'] = self.categorize_article(
                    article['title'], 
                    article['snippet']
                )
                
                # 중요도 점수
                article['importance_score'] = self.calculate_importance(
                    article['title'],
                    article['source'],
                    article['is_recent']
                )
                
                # 한글 번역
                article['title_ko'] = self.translate_to_korean(article['title'])
                article['snippet_ko'] = self.translate_to_korean(article['snippet'])
                
                # 회사 정보
                article['company'] = company
                
                all_articles.append(article)
                
                if len(all_articles) >= target_count:
                    break
            
            if len(all_articles) >= target_count:
                break
            
            time.sleep(1)  # Rate limiting
        
        # 정렬: 우선 출처 > 중요도 > 최신순
        all_articles.sort(key=lambda x: (
            -1 if any(p in x['source'] for p in self.PRIORITY_SOURCES) else 0,
            -x['importance_score'],
            x['published_date']
        ), reverse=True)
        
        print(f"  ✅ Found {len(all_articles)} articles")
        return all_articles[:100]  # 최대 100개
    
    def collect_all_news(self):
        """모든 기업 뉴스 수집"""
        print("\n" + "="*60)
        print("🚀 BigTech News Crawler Started")
        print("="*60)
        
        for company, keywords in self.COMPANIES.items():
            articles = self.collect_news_for_company(company, keywords, target_count=50)
            self.news_data[company] = articles
            time.sleep(2)  # Rate limiting
        
        print("\n" + "="*60)
        print("✅ Collection Completed!")
        print("="*60)
    
    def generate_json(self):
        """JSON 데이터 생성"""
        stats = {}
        for company, articles in self.news_data.items():
            stats[f'{company}_count'] = len(articles)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'statistics': stats,
            'news': self.news_data,
            'metadata': {
                'total_articles': sum(stats.values()),
                'companies': list(self.COMPANIES.keys()),
                'collection_date': datetime.now().strftime('%Y-%m-%d'),
                'cutoff_days': 14,
                'priority_sources': self.PRIORITY_SOURCES,
                'generated_by': 'Free BigTech News Crawler v1.0'
            }
        }
    
    def save_to_file(self, filename='bigtech_data_latest.json'):
        """JSON 파일 저장"""
        data = self.generate_json()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        total = data['metadata']['total_articles']
        print(f"\n💾 Saved {total} articles to {filename}")
        
        # 기업별 통계 출력
        print("\n📊 Statistics:")
        for company, count in data['statistics'].items():
            print(f"  {company}: {count}")


def main():
    """메인 실행 함수"""
    try:
        crawler = BigTechNewsCrawler()
        crawler.collect_all_news()
        crawler.save_to_file()
        
        print("\n🎉 Success! News data updated.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
