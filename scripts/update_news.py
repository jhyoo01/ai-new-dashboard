#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI News Updater for GitHub Pages
실제 AI 뉴스를 크롤링하고 index.html을 업데이트합니다.
"""

import os
import re
import json
import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import quote_plus, urlparse
import hashlib


class AINewsUpdater:
    """AI 뉴스 자동 업데이트"""
    
    def __init__(self):
        self.news_data = []
        self.categories = {
            'chatgpt': ['ChatGPT', 'GPT-4', 'GPT-5', 'OpenAI'],
            'gemini': ['Gemini', 'Google AI', 'Bard'],
            'deepseek': ['DeepSeek', 'DeepSeek-V3', 'DeepSeek AI'],
            'qwen': ['Qwen', 'Qwen 2.5', 'Alibaba AI'],
            'kimi': ['Kimi', 'Kimi-K2', 'Moonshot AI']
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.target_sources = ['theverge.com', 'techcrunch.com']  # 주요 출처
    
    def translate_to_korean(self, text):
        """Google Translate API를 사용한 한글 번역"""
        if not text or len(text.strip()) == 0:
            return text
        
        try:
            # Google Translate 무료 API 사용
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'en',  # source language: English
                'tl': 'ko',  # target language: Korean
                'dt': 't',
                'q': text
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                result = response.json()
                # 번역된 텍스트 추출
                translated = ''.join([item[0] for item in result[0] if item[0]])
                return translated
            else:
                print(f"    번역 실패: {response.status_code}")
                return text
        except Exception as e:
            print(f"    번역 오류: {e}")
            return text
    
    def search_ai_news(self):
        """실제 AI 뉴스 검색"""
        print("🔍 실제 AI 뉴스 검색 중...")
        
        # 특정 AI 모델 중심 키워드
        keywords = [
            'ChatGPT OpenAI',
            'Google Gemini AI',
            'DeepSeek AI',
            'Qwen Alibaba',
            'Kimi Moonshot AI',
            'ChatGPT news',
            'Gemini update',
            'DeepSeek model',
            'Qwen LLM',
            'Kimi-K2 thinking',
            'OpenAI GPT',
            'Google AI',
            'DeepSeek V3',
            'Qwen 2.5',
            'Moonshot AI'
        ]
        
        for keyword in keywords:
            try:
                print(f"  검색 중: {keyword}")
                news = self.fetch_real_news(keyword, max_items=10)  # 키워드당 10개
                self.news_data.extend(news)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"⚠️  {keyword} 검색 실패: {e}")
        
        # 중복 제거
        seen = set()
        unique_news = []
        for item in self.news_data:
            title_hash = hashlib.md5(item['title'].encode()).hexdigest()
            if title_hash not in seen:
                seen.add(title_hash)
                unique_news.append(item)
        
        # 중요도순 정렬
        unique_news.sort(key=lambda x: x['importance'], reverse=True)
        self.news_data = unique_news[:100]  # 최대 100개
        
        print(f"✅ {len(self.news_data)}개 뉴스 수집 완료")
        return self.news_data
    
    def fetch_real_news(self, keyword, max_items=10):
        """실제 뉴스 검색 (Google News RSS 활용)"""
        news_items = []
        
        try:
            # Google News RSS 피드 사용
            rss_url = f"https://news.google.com/rss/search?q={quote_plus(keyword)}&hl=en-US&gl=US&ceid=US:en"
            
            response = requests.get(rss_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return news_items
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')[:max_items * 2]  # 필터링 고려해서 2배 수집
            
            for item in items:
                try:
                    title = item.title.text if item.title else ""
                    link = item.link.text if item.link else ""
                    pub_date = item.pubDate.text if item.pubDate else ""
                    description = item.description.text if item.description else ""
                    source = item.source.text if item.source else "News"
                    
                    # 출처 필터링 (theverge.com, techcrunch.com 우선)
                    link_lower = link.lower()
                    is_target_source = any(target in link_lower for target in self.target_sources)
                    
                    # 설명에서 HTML 태그 제거
                    description_clean = BeautifulSoup(description, 'html.parser').get_text()
                    description_clean = description_clean[:200] + "..." if len(description_clean) > 200 else description_clean
                    
                    # 발행 시간 계산
                    time_ago = self.calculate_time_ago(pub_date)
                    
                    # 카테고리 분류
                    category = self.classify_category(title + " " + description_clean)
                    
                    # 중요도 계산 (우선 출처에 가중치)
                    importance = self.calculate_importance(title, source, is_target_source)
                    
                    # 키워드 추출
                    keywords_list = self.extract_keywords(title, keyword)
                    
                    # 한글 번역
                    print(f"    번역 중: {title[:50]}...")
                    title_ko = self.translate_to_korean(title)
                    description_ko = self.translate_to_korean(description_clean) if description_clean else f"{title_ko}에 대한 최신 소식입니다."
                    
                    news_items.append({
                        'id': len(self.news_data) + len(news_items) + 1,
                        'title': title_ko,  # 한글 제목
                        'source': source,
                        'category': category,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'time': time_ago,
                        'importance': importance,
                        'description': description_ko,  # 한글 설명
                        'link': link,
                        'keywords': keywords_list
                    })
                    
                    # max_items 도달 시 중단
                    if len(news_items) >= max_items:
                        break
                    
                    # 번역 API rate limit 방지
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"    항목 처리 실패: {e}")
                    continue
                    
        except Exception as e:
            print(f"  RSS 피드 가져오기 실패: {e}")
        
        return news_items
    
    def calculate_time_ago(self, pub_date_str):
        """발행 시간 계산"""
        try:
            from email.utils import parsedate_to_datetime
            pub_date = parsedate_to_datetime(pub_date_str)
            now = datetime.now(pub_date.tzinfo)
            diff = now - pub_date
            
            hours = diff.total_seconds() / 3600
            if hours < 1:
                return f"{int(diff.total_seconds() / 60)}분 전"
            elif hours < 24:
                return f"{int(hours)}시간 전"
            else:
                return f"{int(hours / 24)}일 전"
        except:
            return "최근"
    
    def calculate_importance(self, title, source, is_target_source=False):
        """중요도 점수 계산"""
        score = 7.0
        
        # 우선 출처 가중치 (theverge.com, techcrunch.com)
        if is_target_source:
            score += 1.5
        
        # 제목 키워드 가중치
        high_impact = ['breakthrough', 'revolutionary', '획기적', 'launch', '출시', 'releases', 'unveils']
        medium_impact = ['update', '업데이트', 'announces', '발표', 'reveals']
        
        title_lower = title.lower()
        for word in high_impact:
            if word in title_lower:
                score += 1.5
                break
        for word in medium_impact:
            if word in title_lower:
                score += 0.8
                break
        
        # 출처 가중치
        premium_sources = ['TechCrunch', 'The Verge', 'MIT', 'Nature', 'Bloomberg', 'Reuters']
        if any(s in source for s in premium_sources):
            score += 1.0
        
        return min(9.5, round(score, 1))
    
    def extract_keywords(self, title, base_keyword):
        """키워드 추출"""
        keywords = [base_keyword.split()[0]]  # 기본 키워드
        
        # 주요 키워드 리스트
        important_words = ['ChatGPT', 'OpenAI', 'Gemini', 'Google', 'DeepSeek', 
                          'Qwen', 'Kimi', 'Moonshot', 'AI', 'LLM', 'GPT']
        
        for word in important_words:
            if word.lower() in title.lower() and word not in keywords:
                keywords.append(word)
                if len(keywords) >= 3:
                    break
        
        return keywords[:3]
    
    def classify_category(self, text):
        """텍스트로 카테고리 분류"""
        text_lower = text.lower()
        
        # 카테고리별 점수 계산
        scores = defaultdict(int)
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    scores[category] += 1
        
        # 가장 높은 점수의 카테고리 반환
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return 'chatgpt'  # 기본값
    
    def generate_html(self):
        """업데이트된 HTML 생성"""
        print("📝 HTML 생성 중...")
        
        if not self.news_data:
            print("⚠️  뉴스 데이터가 없습니다. 기본 데이터를 사용합니다.")
            self.news_data = self.get_default_news()
        
        # JavaScript 데이터 부분 생성
        news_json = json.dumps(self.news_data, ensure_ascii=False, indent=8)
        
        # 기존 HTML 템플릿 읽기
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # NEWS_DATA 부분 교체
        pattern = r'const NEWS_DATA = \[.*?\];'
        replacement = f'const NEWS_DATA = {news_json};'
        
        updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
        
        # 날짜 업데이트
        current_date = datetime.now().strftime('%Y-%m-%d')
        updated_html = re.sub(
            r"date: '\d{4}-\d{2}-\d{2}'",
            f"date: '{current_date}'",
            updated_html
        )
        
        return updated_html
    
    def get_default_news(self):
        """기본 뉴스 데이터 (실패 시 폴백)"""
        return [
            {
                'id': 1,
                'title': 'OpenAI 최신 AI 모델 발표',
                'source': 'TechCrunch',
                'category': 'chatgpt',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': '2시간 전',
                'importance': 9.5,
                'description': 'OpenAI가 최신 AI 모델을 공개하며 업계에 새로운 기준을 제시했습니다.',
                'link': 'https://www.google.com/search?q=OpenAI+latest+news',
                'keywords': ['OpenAI', 'AI', 'ChatGPT']
            },
            {
                'id': 2,
                'title': 'Google Gemini 주요 업데이트',
                'source': 'The Verge',
                'category': 'gemini',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': '4시간 전',
                'importance': 8.8,
                'description': 'Google이 Gemini의 대규모 업데이트를 발표했습니다.',
                'link': 'https://www.google.com/search?q=Google+Gemini+update',
                'keywords': ['Google', 'Gemini', 'AI']
            },
            {
                'id': 3,
                'title': 'DeepSeek 새로운 모델 출시',
                'source': 'Ars Technica',
                'category': 'deepseek',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': '6시간 전',
                'importance': 8.5,
                'description': 'DeepSeek이 혁신적인 새 모델을 공개했습니다.',
                'link': 'https://www.google.com/search?q=DeepSeek+AI+model',
                'keywords': ['DeepSeek', 'AI', 'LLM']
            }
        ]
    
    def save_html(self, html_content):
        """HTML 파일 저장"""
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("✅ index.html 업데이트 완료!")
    
    def run(self):
        """전체 프로세스 실행"""
        print("🚀 AI News Updater 시작...")
        print("=" * 60)
        
        try:
            # 1. 뉴스 수집
            self.search_ai_news()
            
            # 2. HTML 생성
            html_content = self.generate_html()
            
            # 3. 저장
            self.save_html(html_content)
            
            print("=" * 60)
            print("✨ 업데이트 완료!")
            print(f"📅 업데이트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📊 총 {len(self.news_data)}개 기사")
            
            # 뉴스 미리보기
            print("\n📰 수집된 뉴스:")
            for i, news in enumerate(self.news_data[:5], 1):
                print(f"{i}. [{news['source']}] {news['title'][:60]}...")
            
            return 0
        
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    """메인 실행"""
    updater = AINewsUpdater()
    return updater.run()


if __name__ == "__main__":
    exit(main())
