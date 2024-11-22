from django.conf import settings
from rest_framework.response import Response
from .models import Exchange
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .serializers import ExchangeSerializer


EXCHANGE_API_URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01'


@api_view(['GET'])
def index(request):
    try:
        # SSL 인증 검증 비활성화
        response = requests.get(EXCHANGE_API_URL, verify=False)
        if response.status_code != 200:
            return Response({'error': '외부 API 호출 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = response.json()
        if not data:
            return Response({'error': '외부 API에서 빈 응답'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 기존 데이터 삭제 후 새 데이터 저장
        exist_response = Exchange.objects.all()
        if exist_response:
            Exchange.objects.all().delete()

        serializer = ExchangeSerializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error in index view: {e}")
        return Response({'error': '서버 내부 오류'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


