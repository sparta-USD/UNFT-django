from django.urls import path
from . import views

urlpatterns = [
    path('', views.UnftList.as_view(), name="unft"),
    path('<int:id>/', views.UnftDetail.as_view(), name="unft_detail"),
]