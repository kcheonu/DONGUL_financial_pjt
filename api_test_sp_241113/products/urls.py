from django.urls import path
from . import views
app_name = "products"
urlpatterns = [
 path('', views.index, name="index"),
#  path('deposits/', views.deposits, name="deposits"),
#  path('savings/', views.savings, name="savings"),
]
