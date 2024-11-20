import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# 대상 URL
url = 'http://www.smbs.biz/ExRate/TodayExRate.jsp'

# Selenium WebDriver 설정
driver = webdriver.Chrome()  # ChromeDriver 경로 필요
driver.get(url)

# HTML 소스 가져오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# table_type7 클래스의 테이블 추출
tables_in_div = soup.find_all('div', {'class': 'table_type7'})

# 모든 테이블 데이터를 저장할 데이터프레임 리스트
all_dataframes = []

# 각 div=table_type7에서 테이블 데이터 추출
for div_idx, div in enumerate(tables_in_div):
    # div 안의 테이블 찾기
    table = div.find('table')
    if not table:
        continue  # 테이블이 없으면 넘어감
    
    # 테이블의 행(row) 추출
    rows = table.find_all('tr')
    
    # 헤더 추출
    headers = [th.text.strip() for th in rows[0].find_all('th')]
    
    # 데이터 추출
    table_data = []
    for row in rows[1:]:
        columns = row.find_all('td')
        row_data = [col.text.strip() for col in columns]
        
        # 데이터 길이를 헤더와 일치시킴
        if len(row_data) > len(headers):
            row_data = row_data[:len(headers)]  # 데이터 잘라냄
        elif len(row_data) < len(headers):
            row_data.extend([''] * (len(headers) - len(row_data)))  # 빈 값 추가
        
        table_data.append(row_data)
    
    # 데이터프레임 생성
    df = pd.DataFrame(table_data, columns=headers)
    # 테이블 번호를 추가하여 구분 (optional)
    df['Table Index'] = div_idx
    all_dataframes.append(df)

# 모든 데이터프레임 합치기
final_dataframe = pd.concat(all_dataframes, ignore_index=True)

# 같은 폴더 내 erg_output.csv로 저장
final_dataframe.to_csv('erg_output.csv', index=False, encoding='utf-8-sig')

# WebDriver 종료
driver.quit()

print("모든 테이블 데이터를 erg_output.csv로 저장 완료!")
