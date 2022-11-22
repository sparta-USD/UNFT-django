from django.urls import path
from deal import views
urlpatterns = [
    path('', views.DealView.as_view(), name="deal_view"),
]