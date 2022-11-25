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
        password = data['password']
        password2 = data['password2']

        # username의 길이가 8자가 넘을 때 예외처리
        if len(data.get("username", "")) > 8:
            raise serializers.ValidationError(
            detail={"username": "username은 8자리 이하로 설정해주세요."})
            
        # password 생성 조건 (8-20자이며 최소 하나 이상의 영문자, 숫자, 특수문자가 필요)
        if password == None:
            raise serializers.ValidationError(
                detail={"password": "비밀번호는 8-20자이며 최소 하나 이상의 영문자, 숫자, 특수문자가 필요합니다."}
            )
        
        # 패스워드 조건 불일치(정규식 표현)
        if not re.search(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',password):
                raise serializers.ValidationError(
                detail={"password": "비밀번호는 8-20자이며 최소 하나 이상의 영문자, 숫자, 특수문자가 필요합니다."}
            )
                
        # 패스워드 재확인 
        if password != password2:
            raise serializers.ValidationError(
                detail={"password": "password가 불일치합니다! 다시 확인해주세요"}
            )
        
        return data
        
    def create(self, validated_data):
        # password2를 validated_data에서 꺼내준 후 user를 create해야 한다!
        password = validated_data.pop("password2", "")
        
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
    
