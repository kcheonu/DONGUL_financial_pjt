from django.http import JsonResponse
from .models import DepositProduct, SavingProduct

# 추천 리스트 반환
def get_recommendlist(request):
    # 이자율 기준 상위 5개 예금 및 적금 상품 추천
    deposit_products = list(DepositProduct.objects.order_by('-interest_rate')[:5].values())
    saving_products = list(SavingProduct.objects.order_by('-interest_rate')[:5].values())

    return JsonResponse({
        'deposit_products': deposit_products,
        'saving_products': saving_products,
    })
