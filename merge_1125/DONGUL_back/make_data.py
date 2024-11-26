import os
import django
import random
import requests
import json
from collections import OrderedDict

# Django 설정 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_pjt_back.settings')  # settings.py 경로 확인 필요
django.setup()

from financial_instruments.models import Deposit, Saving  # Django 초기화 후 import
from accounts.models import User

# 사용자 정의 함수
first_name_samples = "송나김이박최정강조윤장임공손전한오서신권황안홍"
middle_name_samples = "찬해지수근민서예지도하주윤채현지혜동희의"
last_name_samples = "의란민혜용준윤우원호후서연아은진"

def random_name():
    """랜덤 이름 생성 함수"""
    return random.choice(first_name_samples) + random.choice(middle_name_samples) + random.choice(last_name_samples)

# API 데이터 가져오기
DP_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
SP_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
API_KEY = 'db6d119bdb8c06afd652e4329d8bc648'

contract_deposit = []
contract_saving = []

params = {
    'auth': API_KEY,
    'topFinGrpNo': '020000',
    'pageNo': 1
}

# 정기예금 데이터 추가
response = requests.get(DP_URL, params=params).json()
for product in response.get('result', {}).get('baseList', []):
    contract_deposit.append(product['fin_prdt_cd'])

# 정기적금 데이터 추가
response = requests.get(SP_URL, params=params).json()
for product in response.get('result', {}).get('baseList', []):
    contract_saving.append(product['fin_prdt_cd'])

# Deposit 및 Saving 데이터베이스 조회
Deposits = Deposit.objects.all()
Savings = Saving.objects.all()

# JSON 파일 생성
save_dir = 'accounts/fixtures/accounts/user_data.json'  # 저장 경로
file = OrderedDict()
name_list = set()
N = 5000  # 생성할 유저 수

with open(save_dir, 'w', encoding="utf-8") as f:
    f.write('[')
    for i in range(N):
        while True:
            rn = random_name()
            if rn not in name_list:
                name_list.add(rn)
                break

        file["model"] = "accounts.User"
        file["pk"] = i + 1
        file["fields"] = {
            'username': f'test{i}',
            'nickname': rn,
            'email': f'test{i}@email.com',
            'contract_deposit': list(
                set(random.sample(list(Deposits.values_list('id', flat=True)), k=random.randint(1, 2)))
            ) if Deposits.exists() else [],
            'contract_saving': list(
                set(random.sample(list(Savings.values_list('id', flat=True)), k=random.randint(2, 3)))
            ) if Savings.exists() else [],
            'age': random.randint(20, 70),
            'money': random.randrange(1000000, 100000000, 1000000),
            'salary': random.randrange(1000000, 150000000, 12000000),
            'password': "a123456789!",
            'desire_amount_saving': random.randrange(50000, 3000000, 100000),
            'desire_amount_deposit': random.randrange(100000, 50000000, 1000000),
            'deposit_period': random.choice([6, 12, 24, 36]),
            'saving_period': random.choice([6, 12, 24, 36]),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False
        }

        json.dump(file, f, ensure_ascii=False, indent="\t")
        if i != N - 1:
            f.write(',')

    f.write(']')
print(f'데이터 생성 완료 / 저장 위치: {save_dir}')
