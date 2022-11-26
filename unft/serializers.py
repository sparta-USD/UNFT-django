from rest_framework import serializers
from .models import Unft

class UnftSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    
    def get_creator(self, obj):
        return obj.creator.username
    def get_owner(self, obj):
        return obj.owner.username
    def get_owner_id(self, obj):
        return obj.owner.id

    class Meta :
        model = Unft
        fields = "__all__"
    

class UnftCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unft
        fields = "__all__"

    def validate(self, data):
        status = data.get("status", False)
        price = data.get("price", 0)

        if not status: # 미판매중일시 price를 0으로 처리
            data['price'] = 0
        else:  
            if price < 0: # 가격 0원이상 넣을 수 있도록 처리
                raise serializers.ValidationError(detail={"price": "0원이상의 숫자만 입력해주세요."})
        
        return data

    def create(self, validated_data):
        return Unft.objects.create(**validated_data)

class UnftUpdateAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unft
        fields = ['title','desc','status','price']

    def validate(self, data):
        status = data.get("status", False)
        price = data.get("price", 0)

        if not status: # 미판매중일시 price를 0으로 처리
            data['price'] = 0
        else:  
            if price < 0: # 가격 0원이상 넣을 수 있도록 처리
                raise serializers.ValidationError(detail={"price": "0원이상의 숫자만 입력해주세요."})
        
        return data


class UnftUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unft
        fields = ['status','price']

    def validate(self, data):
        status = data.get("status", False)
        price = data.get("price", 0)

        if not status: # 미판매중일시 price를 0으로 처리
            data['price'] = 0
        else:  
            if price < 0: # 가격 0원이상 넣을 수 있도록 처리
                raise serializers.ValidationError(detail={"price": "0원이상의 숫자만 입력해주세요."})
        
        return data
      
