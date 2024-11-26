from django.db import models

# 예금 상품 모델
class DepositProduct(models.Model):
    name = models.CharField(max_length=100)  # 상품명
    bank = models.CharField(max_length=100)  # 은행명
    interest_rate = models.FloatField()  # 이자율
    term = models.IntegerField(help_text="기간(개월)")  # 예치 기간

    def __str__(self):
        return self.name

# 적금 상품 모델
class SavingProduct(models.Model):
    name = models.CharField(max_length=100)  # 상품명
    bank = models.CharField(max_length=100)  # 은행명
    interest_rate = models.FloatField()  # 이자율
    term = models.IntegerField(help_text="기간(개월)")  # 예치 기간

    def __str__(self):
        return self.name
