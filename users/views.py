from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, LogoutSerializer

from users.models import User
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)


# 회원가입
class UserView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            
# 로그인                            
class SigninView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
        
# 로그아웃   
class LogoutView(APIView):
    serializer = LogoutSerializer
    permission = (permissions.IsAuthenticated,)
    
    def post (self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"로그아웃 완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)  
        
          
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer