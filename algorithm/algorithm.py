import pandas as pd
from pprint import pprint
import json
import os
# from geopy.distance import geodesic  # 거리 계산을 위한 라이브러리 (예시)

# 금감원 api키로 데이터 받아오기.
import requests
api_key = 'db6d119bdb8c06afd652e4329d8bc648'
# for i in range(1, 50):
url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth=db6d119bdb8c06afd652e4329d8bc648&topFinGrpNo=020000&pageNo=1'
response = requests.get(url)

output_dir = "C:/Users/SSAFY/Desktop/folder/pjt-10/algorithm/"
os.makedirs(output_dir, exist_ok=True)

if response.status_code == 200:
    goods_data = response.json()
    with open(os.path.join(output_dir, 'output.txt'), 'w', encoding='utf-8') as file:
        json.dump(goods_data, file, indent=4, ensure_ascii=False)
    pprint(goods_data)
else:
    print(f'Failed to fetch data. status code : {response.status_code}')

# dcls_end_day : 공시 종료일
# dcls_month : 공시제출월[YYYYMM]
# dcls_strt_day : 공시 시작일
# etc_note : 기타 유의 사항
# fin_co_no : 금융회사 코드
# fin_co_subm_day : 금융회사 제출일[YYYYMMDDHH24MI]
# fin_prdt_cd : 금융상품 코드
# fin_prdt_nm : 금융 상품명
# join_deny : 가입제한 Ex) 1:제한없음, 2:서민전용, 3:일부제한
# join_member : 가입대상
# join_way : 가입 방법
# kor_co_nm : 금융회사 명
# max_limit : 최고한도
# mtrt_int : 만기 후 이자율
# spcl_cnd : 우대조건

# 데이터 : {"
# dcls_month":"201609",
# "fin_co_no":"0010001",
# "fin_prdt_cd":"WR0001A",
# "kor_co_nm":"우리은행",
# "fin_prdt_nm":"우리웰리치 주거래예금",
# "join_way":"영업점,인터넷,스마트폰",
# "mtrt_int":"만기 후
# - 1개월이내 : 만기시점약정이율×50%
# - 1개월초과 6개월이내: 만기시점약정이율×30%
# - 6개월초과 : 만기시점약정이율×20%
# 
# ※ 만기시점 약정이율 : 일반정기예금 금리",
# "spcl_cnd":"다음 중 하나 충족한 입금건에 대해  최고 연0.2%p
# 순신규고객
# 가계대출이용고객
# 입금일 전월 주거래우대조건 2가지이상
# 건별3천만원이상
# 건별 만기 자동재예치",
# "join_deny":"1",
# "join_member":"실명의 개인",
# "etc_note":"
# -추가입금은 신규가입 시 선택한 예치기간을 각 입금건별 입금일로부터 적용
# -재예치는 입금건별 최초 입금일로부터 최장 10년간 가능",
# "max_limit":null,
# "dcls_strt_day":"20160920",
# "dcls_end_day":null,
# "fin_co_subm_day":"201609201028"


# # 가상 데이터 생성
# goods_data = [
#     {
#         '상품명': f'예금 A{i}', 
#         '대면 방식': '대면' if i % 2 == 0 else '비대면', 
#         '금리': round(2.0 + (i % 5) * 0.1, 2),
#         '우대금리': round(0.5 if i % 3 == 0 else 0.3, 2),
#         '저축 기간': (6 + (i % 4) * 6), 
#         '저축 금액 상한선': 5000000 + (i % 5) * 1000000,
#         '선호 은행': f'은행{(i % 5) + 1}', 
#         '연령대': (20 + (i % 4) * 10),
#         '주소 위치': f'위치{(i % 7) + 1}',
#         '평점': round(3.5 + (i % 5) * 0.2, 2)
#     } for i in range(1, 51)
# ]

# 데이터프레임으로 변환
df = pd.DataFrame(goods_data)
print("가상 금융 상품 데이터 (상위 10개):")
print(df.head(10))

# 은행 지점 위치 정보를 담은 예시 데이터
branch_locations = {
    '은행1': [(37.5665, 126.9780), (37.5700, 126.9830)],  # 예: 서울 중심부
    '은행2': [(37.5500, 126.9900)],
    '은행3': [(37.5800, 126.9760), (37.5850, 126.9820)],
    '은행4': [(37.5600, 126.9750)],
    '은행5': [(37.5650, 126.9800), (37.5665, 126.9775)],
}

# 우대금리 조건 충족 여부 확인 함수
def check_preferred_conditions(user, product):
    preferred_conditions = product.get('우대 조건', {})
    is_eligible = True

    # 자동이체 조건
    if preferred_conditions.get('자동이체') and not user.get('자동이체 설정'):
        is_eligible = False
    
    # 급여 이체 조건
    if preferred_conditions.get('급여이체') and not user.get('급여 이체 설정'):
        is_eligible = False
    
    # 주거래 은행 여부 확인
    if preferred_conditions.get('주거래 은행') and user.get('주거래 은행') != product['선호 은행']:
        is_eligible = False
    
    # 특정 나이대 조건
    if '나이대' in preferred_conditions:
        min_age, max_age = preferred_conditions['나이대']
        if not (min_age <= user.get('나이', 0) <= max_age):
            is_eligible = False

    return is_eligible

# 가중치 및 추천 알고리즘 (저축 기간과 우대 금리 적용)
def calculate_weighted_score(interest_rate, bonus_rate, rating, preferred_bank, bank_name, branch_count, distance=None, age=30, service_type="비대면", saving_period=None, product_period=None, user=None, product=None, min_rating_threshold=3.5, preferred_bank_weight=1.2, branch_weight=0.1, distance_weight=0.05):
    # 평점이 기준 미만이면 점수를 0으로 설정해 추천에서 제외
    if rating < min_rating_threshold:
        return 0  # 추천에서 제외될 수 있도록 낮은 점수 반환

    # 주거래 은행 가중치 적용
    if bank_name == preferred_bank:
        interest_rate *= preferred_bank_weight

    # 우대금리 조건 충족 여부 확인
    if check_preferred_conditions(user, product):
        interest_rate += bonus_rate  # 우대 조건을 충족할 때 우대 금리 적용

    # 대면 서비스 선호 사용자 및 고령층(50대 이상)의 경우 점포 수 및 거리 가중치 적용
    if age >= 50 or (service_type == "대면" and distance is not None):
        weighted_score = interest_rate + rating + (branch_count * branch_weight) - (distance * distance_weight)
    else:
        weighted_score = interest_rate + rating  # 비대면 서비스의 경우 거리 무시

    return weighted_score

# 추천 알고리즘 함수
def recommend_savings_products(data, user, preferred_banks, preferred_bank, main_bank_interest, user_location=None, service_type="비대면", user_saving_period=None, interest_tolerance=0.2, min_interest_rate=0.0, top_n=5):
    recommended_products = []
    alternate_recommendations = []  # 대체 추천 리스트 추가
    
    for product in data:
        # 대면 서비스 선호 사용자 또는 고령층에 대해 거주지와의 거리 계산
        distance = None
        if (service_type == "대면" or user['나이'] >= 50) and user_location and product['선호 은행'] in branch_locations:
            branch_distances = [geodesic(user_location, branch).kilometers for branch in branch_locations[product['선호 은행']]]
            distance = min(branch_distances)  # 가장 가까운 지점과의 거리

        # 사용자의 저축 기간과 상품의 저축 기간 일치 여부 확인
        if product.get('저축 기간') == user_saving_period:
            # 우대 조건 충족 여부에 따라 추천 또는 대체 추천 리스트에 추가
            if check_preferred_conditions(user, product):
                weighted_score = calculate_weighted_score(
                    product['금리'],
                    product['우대금리'],
                    product['평점'],
                    preferred_bank,
                    product['선호 은행'],
                    product.get('점포 수', 0),
                    distance,
                    age=user['나이'],
                    service_type=service_type,
                    saving_period=user_saving_period,
                    product_period=product.get('저축 기간'),
                    user=user,
                    product=product
                )
                if weighted_score > 0:
                    product['종합 점수'] = weighted_score
                    recommended_products.append(product)
            else:
                # 우대 조건 미충족 시 대체 추천 리스트에 추가
                alternate_score = calculate_weighted_score(
                    product['금리'],
                    product['우대금리'],
                    product['평점'],
                    preferred_bank,
                    product['선호 은행'],
                    product.get('점포 수', 0),
                    distance,
                    age=user['나이'],
                    service_type=service_type,
                    saving_period=user_saving_period,
                    product_period=product.get('저축 기간'),
                    user=user,
                    product=product
                )
                product['종합 점수'] = alternate_score
                alternate_recommendations.append(product)
    
    # 종합 점수 기준으로 정렬하여 상위 top_n개의 상품을 추천
    sorted_recommended = sorted(recommended_products, key=lambda x: x['종합 점수'], reverse=True)
    sorted_alternate = sorted(alternate_recommendations, key=lambda x: x['종합 점수'], reverse=True)

    return sorted_recommended[:top_n], sorted_alternate[:top_n]

# 사용자 정보 및 선호 조건 설정
user = {
    '나이': 30,
    '자동이체 설정': True,
    '급여 이체 설정': False,
    '주거래 은행': '은행1',
}

# 예시 상품 데이터 설정
data = df.to_dict(orient='records')  # 생성된 가상 데이터를 딕셔너리로 변환

# 추천 목록 생성
preferred_banks = ['은행1', '은행2']
preferred_bank = '은행1'
main_bank_interest = 2.0  # 주거래 은행 금리
user_location = (37.5665, 126.9780)
service_type = "비대면"
user_saving_period = 12

recommended, alternate = recommend_savings_products(data, user, preferred_banks, preferred_bank, main_bank_interest, user_location=user_location, service_type=service_type, user_saving_period=user_saving_period)

# 추천 결과 출력
print("추천 상품 리스트:")
for product in recommended:
    print(f"상품명: {product['상품명']}, 은행명: {product['선호 은행']}, 금리: {product['금리']}%, 저축 기간: {product.get('저축 기간')}개월, 평점: {product['평점']}, 종합 점수: {product['종합 점수']:.2f}")

print("\n대체 추천 상품 리스트:")
for product in alternate:
    print(f"상품명: {product['상품명']}, 은행명: {product['선호 은행']}, 금리: {product['금리']}%, 저축 기간: {product.get('저축 기간')}개월, 평점: {product['평점']}, 종합 점수: {product['종합 점수']:.2f}")