from konlpy.tag import Okt
from collections import Counter

# 1. 텍스트 파일 불러오기
with open("text/1.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. 형태소 분석기 초기화
okt = Okt()

# 3. 문장 분리 → 명사 추출
lines = text.split('\n')  # 줄 단위 자르기
nouns = []
for line in lines:
    nouns += okt.nouns(line)

# 4. 불용어 제거
stopwords = ['이', '그', '저', '것', '을', '는', '에', '의', '가', '과', '와', '도', '하다', '되다']
clean_nouns = [n for n in nouns if n not in stopwords and len(n) > 1]

# 5. 빈도수 계산
counter = Counter(clean_nouns)
most_common = counter.most_common(30)

# 6. 출력
print("📌 전체 명사 추출 (샘플 30개):", nouns[:30])
print("📌 불용어 제거 후 (샘플 30개):", clean_nouns[:30])
print("📌 총 단어 수:", len(clean_nouns))
print("📌 상위 30개 핵심어")
for word, freq in most_common:
    print(f"{word}: {freq}")
