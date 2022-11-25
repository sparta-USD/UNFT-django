from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('signin/', views.SigninView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('password_reset/',views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
]
