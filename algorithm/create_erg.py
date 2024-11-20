import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def fetch_and_append_exchange_rate_data(url, output_file):
    """
    환율 데이터를 크롤링하고 기존 CSV 파일에 데이터를 추가합니다.
    Args:
        url (str): 크롤링 대상 URL.
        output_file (str): 저장할 CSV 파일 경로.
    """

    # WebDriver 초기화
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # 페이지 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table_type7'))
        )
    except Exception as e:
        print("페이지 로드 실패:", e)
        driver.quit()
        return

    # HTML 소스 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 오늘의 날짜 데이터
    today_date = datetime.now().strftime('%Y-%m-%d')

    # 테이블 데이터 저장용 리스트
    all_data = []

    # table_type7 클래스의 모든 div를 찾아 반복
    for div in soup.find_all('div', {'class': 'table_type7'}):
        table = div.find('table')
        if not table:
            continue

        # 행과 열 데이터 추출
        rows = table.find_all('tr')
        if not rows:
            continue  # rows가 비어 있으면 다음으로 넘어감

        # 헤더 추출
        headers = [th.text.strip() for th in rows[0].find_all('th')]

        # 'Cross Rate' 헤더 제거 (필요 없는 열 제거)
        if 'Cross Rate' in headers:
            headers.remove('Cross Rate')

        for row in rows[1:]:
            row_data = [td.text.strip() for td in row.find_all('td')]

            # 'Cross Rate' 값 제외 (해당 인덱스 제거)
            if 'Cross Rate' in headers:
                cross_rate_index = headers.index('Cross Rate')
                if cross_rate_index < len(row_data):
                    del row_data[cross_rate_index]

            # 헤더와 데이터 길이 맞추기
            if len(row_data) < len(headers):
                row_data += [''] * (len(headers) - len(row_data))  # 부족한 부분 채우기
            elif len(row_data) > len(headers):
                row_data = row_data[:len(headers)]  # 초과 데이터 제거

            all_data.append(row_data + [today_date])  # 날짜 추가

    # 필요한 열만 설정
    if '통화명' in headers and '환율(원)' in headers:
        headers = ['통화명', '환율(원)', '전일대비', 'Date']
    else:
        print("필수 열이 데이터에 없습니다.")
        driver.quit()
        return

    # 데이터프레임 생성
    if all_data and headers:  # 데이터가 있는 경우에만 생성
        new_data = pd.DataFrame(all_data, columns=headers)

        # 기존 파일 읽기
        try:
            existing_data = pd.read_csv(output_file, encoding='utf-8-sig')
        except FileNotFoundError:
            existing_data = pd.DataFrame(columns=headers)

        # 기존 데이터와 새로운 데이터 병합
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)

        # 중복 제거 및 저장
        combined_data.drop_duplicates(inplace=True)
        combined_data.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"환율 데이터를 {output_file}에 추가 저장 완료!")
    else:
        print("데이터가 없어서 CSV를 생성하지 않았습니다.")

    driver.quit()

# 한글 폰트 설정
def set_korean_font():
    import platform
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')  # Windows
    elif platform.system() == 'Darwin':
        plt.rc('font', family='AppleGothic')  # macOS
    else:
        plt.rc('font', family='NanumGothic')  # Linux
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

def plot_exchange_rate(input_file):
    """
    CSV 파일에서 데이터를 읽어 통화명별로 날짜별 환율 변화를 그래프로 그립니다.
    Args:
        input_file (str): CSV 파일 경로.
    """
    try:
        # CSV 파일 읽기
        data = pd.read_csv(input_file, encoding='utf-8-sig')
    except FileNotFoundError:
        print(f"{input_file} 파일이 존재하지 않습니다.")
        return

    # 필요한 열만 처리
    if '환율(원)' in data.columns:
        data['환율'] = data['환율(원)'].str.replace(',', '').astype(float)
    else:
        print("'환율(원)' 열이 없습니다.")
        return

    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
    else:
        print("'Date' 열이 없습니다.")
        return

    if '통화명' not in data.columns:
        print("'통화명' 열이 없습니다.")
        return

    # 그래프를 생성할 통화명 목록
    # 그래프를 생성할 나라 목록 : [미국, 중국(위안), 일본 엔, 유로, 영국 파운드, 캐나다 달러, 스위스 프랑, 호주 달러, 홍콩 달러, 대만 달러, 싱가포르 달러]
    target_currencies = [
        "미국 달러 (USD)", "위안 (CNH)", "일본 엔 (JPY) (100)", "유로 (EUR)", "영국 파운드 (GBP)", 
        "캐나다 달러 (CAD)", "스위스 프랑 (CHF)", "호주 달러 (AUD)", "홍콩 달러 (HKD)", 
        "대만 달러 (TWD)", "싱가포르 달러 (SGD)"
    ]

    # 대상 통화만 필터링
    data = data[data['통화명'].isin(target_currencies)]

    # 한글 폰트 설정
    set_korean_font()

    # 통화명 기준으로 그룹화
    grouped = data.groupby('통화명')

    # 그래프 생성
    for name, group in grouped:
        plt.figure(figsize=(10, 6))
        plt.plot(group['Date'], group['환율'], marker='o', label=name)
        plt.title(f"{name} 환율 변화", fontsize=16)
        plt.xlabel("날짜", fontsize=12)
        plt.ylabel("환율 (KRW)", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{name.replace(' ', '_').replace('/', '_')}_환율_변화.png")  # 그래프 저장

    print("선택한 통화명별 그래프 생성 완료!")



# URL 및 출력 파일 경로 설정
target_url = 'http://www.smbs.biz/ExRate/TodayExRate.jsp'
output_csv = 'erg_output.csv'

# 데이터 가져오기 및 저장 (매일 아침 08시 실행되도록 해야함.)
fetch_and_append_exchange_rate_data(target_url, output_csv)

# 데이터 읽어서 그래프 생성
plot_exchange_rate(output_csv)

# 지금은 CSV파일에서 읽어서 오지만 추후에는 DB에서 데이터를 읽고 그래프를 그려가야함.

