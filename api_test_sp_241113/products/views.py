from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.http import JsonResponse

API_KEY = settings.API_KEY
# 예금: deposit 적금: saving
@api_view(["GET"])
def index(request):
    url = "http://finlife.fss.or.kr/finlifeapi/companySearch.json"
    auth = settings.API_KEY
    params = {
        "auth" : auth,
        "topFinGrpNo" : "020000",
        "pageNo" : "1"
        
    }
    response = requests.get(url, params=params).json()
    return JsonResponse(response)