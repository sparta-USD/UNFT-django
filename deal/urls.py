from django.urls import path
from deal import views
urlpatterns = [
    path('', views.DealView.as_view(), name="deal_view"),
    path('<int:id>/', views.DealDetailView.as_view(), name="deal_detail_view"),
    path('complete/<int:id>/', views.DealCompleteView.as_view(), name="deal_complete_view"),
]