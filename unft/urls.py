from django.urls import path
from . import views

urlpatterns = [
    path('', views.UnftList.as_view(), name="Unft"),
]