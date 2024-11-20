import pandas as pd
import json
import os
import requests
import re

# API 호출
api_key = 'db6d119bdb8c06afd652e4329d8bc648'
url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'

response = requests.get(url)
output_dir = "C:/Users/SSAFY/Desktop/folder/pjt-10/algorithm/"  # 데이터를 저장할 디렉토리 경로
os.makedirs(output_dir, exist_ok=True)

# 데이터 저장 디버깅
if response.status_code == 200:
    goods_data = response.json()
    print("데이터를 파일에 저장합니다...")
    with open(os.path.join(output_dir, 'output2.txt'), 'w', encoding='utf-8') as file:
        json.dump(goods_data, file, indent=4, ensure_ascii=False)
    print(f"데이터가 파일에 성공적으로 저장되었습니다: {output_dir}/output2.txt")
else:
    raise Exception(f"Failed to fetch data. Status code: {response.status_code}")


# 데이터프레임 생성
base_list = pd.DataFrame(goods_data["result"]["baseList"])
option_list = pd.DataFrame(goods_data["result"]["optionList"])

# baseList와 optionList 병합
merged_data = pd.merge(base_list, option_list, on="fin_prdt_cd", how="inner")

# 우대 조건 정형화 함수
def standardize_special_conditions(spcl_cnd):
    if not spcl_cnd or spcl_cnd.strip() == "":
        return "우대조건 없음"
    
    conditions = []
    if re.search(r"자동이체", spcl_cnd):
        conditions.append("자동이체")
    if re.search(r"급여이체", spcl_cnd):
        conditions.append("급여이체")
    if re.search(r"신규고객", spcl_cnd):
        conditions.append("신규고객")
    if re.search(r"평잔", spcl_cnd):
        conditions.append("월평균잔액")
    if re.search(r"카드결제", spcl_cnd):
        conditions.append("카드결제실적")

    return ", ".join(conditions) if conditions else "우대조건 없음"

# spcl_cnd 정형화
merged_data["standardized_spcl_cnd"] = merged_data["spcl_cnd"].apply(standardize_special_conditions)

# 우대 조건 분석 함수
def analyze_preferred_conditions(consumer, product):
    conditions = product["standardized_spcl_cnd"].split(", ")
    bonus_rate = 0.0

    if "자동이체" in conditions and consumer.get("auto_transfer", False):
        bonus_rate += 0.1
    if "급여이체" in conditions and consumer.get("salary_transfer", False):
        bonus_rate += 0.1
    if "신규고객" in conditions and consumer.get("new_customer", False):
        bonus_rate += 0.2
    if "월평균잔액" in conditions and consumer.get("monthly_balance", 0) >= 3000000:
        bonus_rate += 0.1
    if "카드결제실적" in conditions and consumer.get("card_usage", False):
        bonus_rate += 0.1

    return bonus_rate

# 금리 계산 및 추천 함수
def recommend_products_with_options(consumer, products, top_n=10):
    recommendations = []

    for _, product in products.iterrows():
        # 사용자의 저축 기간과 상품의 기간(save_trm) 매칭
        if int(product["save_trm"]) != consumer["saving_period"]:
            continue

        # 기본 금리와 우대 금리 계산
        base_rate = float(product.get("intr_rate", 0))
        bonus_rate = float(product.get("intr_rate2", 0))
        user_bonus_rate = analyze_preferred_conditions(consumer, product)
        final_rate = max(base_rate, bonus_rate + user_bonus_rate)

        recommendations.append({
            "금융회사명": product["kor_co_nm"],
            "금융상품명": product["fin_prdt_nm"],
            "기본 금리": round(base_rate, 2),
            "우대 금리": round(bonus_rate, 2),
            # "소비자 우대 금리": round(user_bonus_rate, 2),
            "최종 금리": round(final_rate, 2),
            "저축 기간": product["save_trm"],
        })

    # 상위 top_n개의 추천 상품 반환
    return sorted(recommendations, key=lambda x: x["최종 금리"], reverse=True)[:top_n]


# 소비자 정보 (예시)
consumer_1 = {
    "age": 30,
    "saving_period": 12,  # 12개월 저축
    "auto_transfer": True,
    "salary_transfer": False,
    "new_customer": True,
    "monthly_balance": 4000000,
    "card_usage": True,
}

consumer_2 = {
    "age": 55,
    "saving_period": 6,  # 6개월 저축
    "auto_transfer": False,
    "salary_transfer": True,
    "new_customer": False,
    "monthly_balance": 2000000,
    "card_usage": False,
}

consumers = [consumer_1, consumer_2]

# 추천 결과 출력
for idx, consumer in enumerate(consumers, start=1):
    print(f"\n소비자 {idx}의 추천 상품 리스트:")
    recommended = recommend_products_with_options(consumer, merged_data)
    # for product in recommended:
    #     print(product)
    #     print(f"금융회사명: {product['금융회사명']}, 금융상품명: {product['금융상품명']}, "
    #           f"기본 금리: {product['기본 금리']}%, 우대 금리: {product['우대 금리']}%, "
    #           f"소비자 우대 금리: {product['소비자 우대 금리']}%, 최종 금리: {product['최종 금리']}%, "
    #           f"저축 기간: {product['저축 기간']}개월")

    with open(os.path.join(output_dir, 'recommended_list.txt'), 'w', encoding='utf-8') as file:
        json.dump(recommended, file, indent=4, ensure_ascii=False)
