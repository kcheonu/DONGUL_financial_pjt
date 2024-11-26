from django.urls import path, include
from . import views



urlpatterns = [
    path('<str:username>/', views.user_profile),
    path('<str:username>/info/', views.user_info),
    path('<str:username>/profile/', views.user_info_profile),
    path('accounts/', include('allauth.urls')),
    # path('load_users_data/', views.load_users_data)
] 
