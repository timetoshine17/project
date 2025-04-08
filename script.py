import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('dcinside_posts_selenium.csv', encoding='utf-8')  # encoding='cp949'일 수도 있음

# 데이터프레임 정보 출력
print("✅ 데이터 정보:")
print(df.info())
print("\n✅ 상위 5개 행:")
print(df.head())

# 결측값 확인
print("\n✅ 결측값 개수:")
print(df.isnull().sum())

# 열 이름 확인
print("\n✅ 열 이름:")
print(df.columns)
