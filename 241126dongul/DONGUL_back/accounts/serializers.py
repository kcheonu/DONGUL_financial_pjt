from rest_framework import serializers
from allauth.account.adapter import get_adapter
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from financials.serializers import ContractDepositSerializer, ContractSavingSerializer



# class CustomRegisterSerializer(RegisterSerializer):
#     # 추가할 필드들을 정의합니다.
#     username = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         max_length=100
#     )
#     name = serializers.CharField(max_length=100)
#     email = serializers.EmailField(required=False)
   
    
#     def get_cleaned_data(self):
#         return {
#             'username': self.validated_data.get('username', ''),
#             'password1': self.validated_data.get('password1', ''),
#             'password2': self.validated_data.get('password2', ''),
#             'name': self.validated_data.get('name', ''),
#             'email': self.validated_data.get('email', ''),
#         }
class CustomRegisterSerializer(RegisterSerializer):
    # 필요한 필드들을 추가합니다.
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255
    )
    age = serializers.CharField(
        required=False,
        allow_blank=True,
    )
    # 해당 필드도 저장 시 함께 사용하도록 설정합니다.
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            # nickname 필드 추가
            'nickname': self.validated_data.get('nickname', ''),
            'age': self.validated_data.get('age', ''),
        }
        
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user

    # def save(self, request):
    #     user = super().save(request)
    #     # 추가 필드 작성
    #     user.nickname = self.validated_data.get('nickname', '')
    #     user.phone = self.validated_data.get('phone', '')
    #     user.age = self.validated_data.get('age', 0)
    #     user.save()
    #     return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_img', 'id', 'username', 'name', 'email', 'age', 'money', 'salary')
        read_only_fields = ('id','username', 'name',)


class UserInfoSerializer(serializers.ModelSerializer):
        profile_img = serializers.ImageField(use_url=True)
        contract_deposit = ContractDepositSerializer(many=True)
        contract_saving = ContractSavingSerializer(many=True)
        class Meta:
            model = User
            fields = '__all__'
            read_only_fields = ('id','username', 'name',)
            
            




