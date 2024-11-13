from rest_framework import serializers
from .models import DepositOptions, DepositProducts, Companies

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = "__all__"
        
class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = "__all__"
        read_only_fields = ("product",)

class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"
        