from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import re #정규식 처리 모듈


class UserSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields=['email', 'username', 'password','password2', 'usd']
        
    def validate(self, data):
        correct_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
        password_input = correct_password.match(data.get("password", ""))
        password = data['password']
        password2 = data['password2']

        if data.get("username"):
            try:
                if User.objects.get(username=data.get("username")):
                    raise serializers.ValidationError(
                        detail={"username": "이미 존재하는 username입니다."}
                    )
            except:
                # username의 길이가 8자가 넘을 때
                if len(data.get("username", "")) > 8:
                    raise serializers.ValidationError(
                    detail={"username": "username은 8자리 이하로 설정해주세요."})
        
        if password_input == None:
            raise serializers.ValidationError(
                detail={"password": "비밀번호는 8-20자이며 최소 하나 이상의 영문자, 숫자, 특수문자가 필요합니다."})
            
        if password != password2:
            raise serializers.ValidationError(
                detail={"password": "password가 불일치합니다! 다시 확인해주세요"}
            )
        
        return data
        
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
    
