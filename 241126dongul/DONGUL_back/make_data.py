import random
import requests

first_name_samples = "김나박이송최정강조윤장임공손전한오서신권황안홍선고양부"
middle_name_samples = "찬해지수근민서예지도하주윤채현지혜동희의시"
last_name_samples = "의란민혜용준윤우원호후서연아은진지아주"

def random_name():
    result = ""
    result += random.choice(first_name_samples)
    result += random.choice(middle_name_samples)
    result += random.choice(last_name_samples)
    return result 

# 현재 API 에 들어있는 금융 상품 코드 리스트 저장
DP_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
SP_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'

API_KEY = '16dd1959199940770f9f4793f549c2a0'

contract_deposit = []
contract_saving = []

params = {
  'auth': API_KEY,
  # 금융회사 코드 020000(은행), 030200(여신전문), 030300(저축은행), 050000(보험), 060000(금융투자)
  'topFinGrpNo': '020000',
  'pageNo': 1
}

# 정기예금 목록 저장
response = requests.get(DP_URL, params=params).json()
baseList = response.get('result').get('baseList')   # 상품 목록

for product in baseList:
    contract_deposit.append(product['fin_prdt_cd'])

# 적금 목록 저장
response = requests.get(SP_URL, params=params).json()
baseList = response.get('result').get('baseList')   # 상품 목록

for product in baseList:
    contract_saving.append(product['fin_prdt_cd'])

dict_keys = ['username', 'gender', 'contract_deposit', 'contract_saving', 'age', 'money', 'salary']

# json 파일 만들기
import json
from collections import OrderedDict

file = OrderedDict()

name_list = []
N = 5000
i = 0

while i < N:
    rn = random_name()
    if rn in name_list:
        continue
    
    name_list.append(rn)
    i += 1

    
# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
save_dir = 'accounts/fixtures/accounts/user_data.json'
with open(save_dir, 'w', encoding="utf-8") as f:
   
    f.write('[')
    for i in range(N):
        # 랜덤한 데이터를 삽입
        file["model"] = "accounts.User"
        file["pk"] = i+1
        file["fields"] = {
            'username': 'test'+str(i), # 유저아이디 test1,2,3,4,5,6,7
            'nickname': name_list[i],  # 유저 이름 랜덤 생성
            # 랜덤한 0~5개의 상품을 가입하도록 삽입됨

            'financial_products': ','.join(map(str, random.sample(contract_deposit + contract_saving, random.randint(1, 5)))),
           
            'age': random.randint(20, 70),  # 나이
            'money': random.randrange(1000000, 100000000, 1000000),    # 현재 가진 금액
            'salary': random.randrange(1000000, 150000000, 12000000), # 연봉
            'password': "a123456789!",
            'desire_amount_saving': random.randrange(50000, 3000000, 100000), #적금 랜덤
            'desire_amount_deposit': random.randrange(100000, 50000000, 1000000), # 예금 랜덤
            'deposit_period':random.choice([6, 12, 24, 36]), # 기간 랜덤
            'saving_period':random.choice([6, 12, 24, 36]), # 기간 랜덤
            'is_active': True,
            'is_staff': False,
            'is_superuser': False
        }
        file['fields']['desire_amount_deposit'] = random.randrange(100000, file['fields']['money'], 1000000)

        json.dump(file, f, ensure_ascii=False, indent="\t")
        if i != N-1:
            f.write(',')

    f.write(']')
    f.close()

print(f'데이터 생성 완료 / 저장 위치: {save_dir}')
