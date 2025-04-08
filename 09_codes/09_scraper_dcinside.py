from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd
from bs4 import BeautifulSoup

# 설정
gallery_name = "tree"  # 갤러리 이름 설정
max_posts = 3   # 스크랩할 게시글 개수 설정

# Selenium 드라이버 설정 (Chrome)
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# DCInside 갤러리 URL 및 기본 설정
gallery_url = f"https://gall.dcinside.com/board/lists/?id={gallery_name}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# 갤러리 페이지 로드
driver.get(gallery_url)
time.sleep(3)  # 페이지 로드를 위한 대기

# 페이지 소스를 BeautifulSoup으로 파싱하여 게시글 목록 추출
soup = BeautifulSoup(driver.page_source, "html.parser")
posts = soup.select("tr.us-post")

results = []
for idx, post in enumerate(posts, start=1):
    title_element = post.select_one("a")
    if title_element:
        # 게시글 제목 및 링크 추출
        title = title_element.get_text(strip=True)
        link = title_element.get("href")
        post_url = "https://gall.dcinside.com" + link
        print(f"현재 {idx}번째 게시글 처리 중: {title}")
        print("게시글 URL:", post_url)
        
        # 개별 게시글 페이지 로드
        driver.get(post_url)
        time.sleep(1 + random.random())  # 페이지 로드 대기
        
        # 페이지 하단으로 스크롤하여 댓글 및 추천/비추천 수가 로드되도록 함
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # 충분한 대기 시간 추가
        
        # 개별 게시글 페이지 파싱
        post_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # 댓글 추출: 댓글은 li 태그의 클래스 "ub-content"로 가정
        comment_tags = post_soup.find_all("li", class_="ub-content")
        comments = [comment.get_text(strip=True) for comment in comment_tags]
        
        print("댓글 개수:", len(comments))
        
        # 추천 및 비추천 수 추출 (Selenium의 find_element 사용)
        try:
            # 추천 수: <p class="up_num font_red"> 요소
            recommend_elem = driver.find_element(By.CSS_SELECTOR, "p.up_num.font_red")
            recommend_count = recommend_elem.text
        except Exception as e:
            recommend_count = "0"
        try:
            # 비추천 수: <p class="down_num"> 요소
            unrecommend_elem = driver.find_element(By.CSS_SELECTOR, "p.down_num")
            unrecommend_count = unrecommend_elem.text
        except Exception as e:
            unrecommend_count = "0"
                 
        print("추천 수:", recommend_count, "비추천 수:", unrecommend_count)
        print("-" * 50)
        
        results.append({
            "title": title,
            "url": post_url,
            "comments": comments,
            "recommend_count": recommend_count,
            "unrecommend_count": unrecommend_count
        })
        
        # 서버 부담을 줄이기 위해 무작위 딜레이 적용
        time.sleep(0.5 + random.random())
        
        # 스크랩할 게시글 개수에 도달하면 크롤링 종료
        if len(results) >= max_posts:
            print(f"설정한 {max_posts}개의 게시글을 모두 스크랩했습니다.")
            break

# 결과를 DataFrame으로 변환 후 CSV로 저장
df = pd.DataFrame(results)
df.to_csv("dcinside_posts_selenium.csv", index=False, encoding="utf-8")
print("크롤링 완료. 데이터가 dcinside_posts_selenium.csv에 저장되었습니다.")

driver.quit()