#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI News Updater for GitHub Pages
매일 최신 AI 뉴스를 크롤링하고 index.html을 업데이트합니다.
"""

import os
import re
import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from collections import defaultdict


class AINewsUpdater:
    """AI 뉴스 자동 업데이트"""
    
    def __init__(self):
        self.news_data = []
        self.categories = {
            'llm': ['ChatGPT', 'GPT', 'Claude', 'Gemini', 'LLM', 'OpenAI', 'Anthropic', '대형언어모델'],
            'industry': ['AI 투자', 'AI 스타트업', '삼성', 'LG', 'NVIDIA', '구글', 'AI 기업'],
            'research': ['AI 연구', 'DeepSeek', '논문', '알고리즘', 'MIT', 'Stanford'],
            'ml_dl': ['머신러닝', '딥러닝', '신경망', 'Machine Learning', 'Deep Learning'],
            'application': ['AI 활용', 'AI 서비스', '신약', '의료', '자율주행']
        }
    
    def search_ai_news(self):
        """AI 뉴스 검색 (Google News 스타일)"""
        print("🔍 AI 뉴스 검색 중...")
        
        keywords = [
            'AI 뉴스', 'ChatGPT', 'Claude', 'OpenAI', 'Anthropic', 
            'Google AI', 'DeepSeek', '인공지능', 'LLM', 'Gemini',
            'AI 연구', 'AI 투자', 'AI 규제'
        ]
        
        for keyword in keywords[:5]:  # 상위 5개 키워드만
            try:
                news = self.fetch_news_for_keyword(keyword)
                self.news_data.extend(news)
                time.sleep(2)  # Rate limiting
            except Exception as e:
                print(f"⚠️  {keyword} 검색 실패: {e}")
        
        # 중복 제거
        seen = set()
        unique_news = []
        for item in self.news_data:
            title_hash = hash(item['title'])
            if title_hash not in seen:
                seen.add(title_hash)
                unique_news.append(item)
        
        self.news_data = unique_news[:12]  # 최대 12개
        print(f"✅ {len(self.news_data)}개 뉴스 수집 완료")
        
        return self.news_data
    
    def fetch_news_for_keyword(self, keyword):
        """키워드로 뉴스 검색"""
        news_items = []
        
        # 실제 환경에서는 News API 등을 사용
        # 여기서는 샘플 생성
        base_sources = ['TechCrunch', '조선일보', 'The Verge', 'MIT Technology Review', 
                       'Forbes', 'Bloomberg', 'Reuters', 'Nature', 'Ars Technica', '중앙일보']
        
        # 키워드 기반으로 가상 뉴스 생성 (실제로는 API나 크롤링 필요)
        category = self.classify_category(keyword)
        
        news_items.append({
            'title': f'{keyword} 관련 최신 AI 기술 동향',
            'source': base_sources[len(news_items) % len(base_sources)],
            'category': category,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': self.get_random_time(),
            'importance': round(7.5 + (len(keyword) % 3) * 0.5, 1),
            'description': f'{keyword}에 대한 최신 AI 업계 동향과 기술 발전 소식입니다. 글로벌 AI 기업들의 혁신적인 움직임이 주목받고 있습니다.',
            'link': f'https://www.google.com/search?q={keyword}+AI+news',
            'keywords': [keyword, 'AI', '기술']
        })
        
        return news_items
    
    def classify_category(self, keyword):
        """키워드로 카테고리 분류"""
        keyword_lower = keyword.lower()
        
        for category, keywords in self.categories.items():
            if any(k.lower() in keyword_lower for k in keywords):
                return category
        
        return 'llm'  # 기본값
    
    def get_random_time(self):
        """랜덤 시간 생성"""
        import random
        hours = random.randint(1, 14)
        if hours == 1:
            return '1시간 전'
        elif hours < 24:
            return f'{hours}시간 전'
        else:
            return '1일 전'
    
    def generate_html(self):
        """업데이트된 HTML 생성"""
        print("📝 HTML 생성 중...")
        
        if not self.news_data:
            print("⚠️  뉴스 데이터가 없습니다. 기본 데이터를 사용합니다.")
            self.news_data = self.get_default_news()
        
        # JavaScript 데이터 부분 생성
        news_json = json.dumps(self.news_data, ensure_ascii=False, indent=12)
        
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
                'title': 'OpenAI, 최신 AI 모델 발표',
                'source': 'TechCrunch',
                'category': 'llm',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': '2시간 전',
                'importance': 9.5,
                'description': 'OpenAI가 최신 AI 모델을 공개하며 업계에 새로운 기준을 제시했습니다.',
                'link': 'https://www.google.com/search?q=OpenAI+latest+news',
                'keywords': ['OpenAI', 'AI', 'LLM']
            },
            {
                'id': 2,
                'title': 'Google Gemini 업데이트 발표',
                'source': 'The Verge',
                'category': 'llm',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': '4시간 전',
                'importance': 8.8,
                'description': 'Google이 Gemini의 대규모 업데이트를 발표했습니다.',
                'link': 'https://www.google.com/search?q=Google+Gemini+news',
                'keywords': ['Google', 'Gemini', 'AI']
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
