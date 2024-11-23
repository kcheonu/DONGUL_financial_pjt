from django.conf import settings
from rest_framework.response import Response
from .models import Exchange
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .serializers import ExchangeSerializer
from datetime import datetime

# API URL 기본 설정
BASE_API_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"

@api_view(['GET'])
def index(request):
    try:
        # 요청에서 데이터 타입 가져오기 (기본값 'AP01')
        data_type = request.GET.get('data', 'AP01')

        # 오늘 날짜 계산
        today = datetime.today().strftime('%Y%m%d')  # 날짜 포맷: YYYYMMDD

        # API URL 생성
        api_url = f"{BASE_API_URL}?authkey={settings.EXCHANGE_API_KEY}&data={data_type}&searchdate={today}"

        # API 호출
        response = requests.get(api_url, verify=False)
        print(f"API 호출 URL: {api_url}")
        print(f"HTTP 응답 상태 코드: {response.status_code}")

        if response.status_code != 200:
            return Response({'error': '외부 API 호출 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # API 응답 데이터 확인
        data = response.json()
        if not data:
            print("API에서 데이터를 반환하지 않았습니다.")
            return Response({'message': '오늘 데이터가 없습니다.'}, status=status.HTTP_204_NO_CONTENT)

        # 데이터 변환: 모델 필드와 매핑
        processed_data = [
            {
                'cur_unit': item.get('cur_unit'),
                'cur_nm': item.get('cur_nm'),
                'ttb': item.get('ttb'),
                'tts': item.get('tts'),
                'deal_bas_r': item.get('deal_bas_r'),
                'bkpr': item.get('bkpr'),
                'yy_efee_r': item.get('yy_efee_r'),
                'ten_dd_efee_r': item.get('ten_dd_efee_r'),
                'kftc_deal_bas_r': item.get('kftc_deal_bas_r'),
                'kftc_bkpr': item.get('kftc_bkpr'),
            }
            for item in data
        ]

        # 중복 데이터 확인 및 추가
        for entry in processed_data:
            # 중복 확인: 동일한 `cur_unit`과 `deal_bas_r` 데이터가 이미 존재하는지 확인
            if not Exchange.objects.filter(cur_unit=entry['cur_unit'], deal_bas_r=entry['deal_bas_r']).exists():
                serializer = ExchangeSerializer(data=entry)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(f"직렬화 오류: {serializer.errors}")

        return Response({'message': '오늘 데이터를 성공적으로 저장했습니다.'}, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류: {e}")
        return Response({'error': f'외부 API 요청 오류: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print(f"서버 내부 오류: {e}")
        return Response({'error': f'서버 내부 오류: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def latest_exchange_rates(request):
    try:
        # DB에서 통화별 최신 데이터를 가져오기
        latest_data_query = """
        SELECT *
        FROM exchange_exchange
        WHERE id IN (
            SELECT MAX(id)
            FROM exchange_exchange
            GROUP BY cur_unit
        )
        ORDER BY cur_unit;
        """
        
        # Raw SQL로 데이터 가져오기
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(latest_data_query)
            rows = cursor.fetchall()

        # 컬럼 이름 매핑
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        # 결과 반환
        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"서버 오류: {e}")
        return Response({"error": "서버 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def selected_currencies(request):
    try:
        # 주요 국가들의 통화 코드
        currencies = ['USD', 'CAD', 'CHF', 'JPY(100)', 'HKD', 'GBP', 'EUR', 'CNH']

        # 특정 통화 데이터 필터링
        selected_data = Exchange.objects.filter(cur_unit__in=currencies).order_by('cur_unit', 'id')

        # 데이터를 직렬화하여 반환
        serializer = ExchangeSerializer(selected_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"서버 오류: {e}")
        return Response({"error": "서버 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)