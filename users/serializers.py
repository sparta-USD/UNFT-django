from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['email', 'username', 'password', 'usd']
        
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
     
    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_admin'] = user.is_admin

        return token
    
    
class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['refresh',]
        
    refresh = serializers.CharField()
    
    default_error_messages = {
        'bad_token': ('토큰이 만료됐거나 유효하지않습니다.')
    }
    
    def validate(self,attrs):
        self.token =attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
    
