from rest_framework import serializers
from .models import Unft

class UnftSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    
    def get_creator(self, obj):
        return obj.creator.username
    def get_owner(self, obj):
        return obj.owner.username
    def get_price(self, obj):
        return obj.price if obj.status else 0

    class Meta :
        model = Unft
        fields = "__all__"

class UnftCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unft
        fields = "__all__"

class UnftUpdateAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unft
        fields = ['title','desc','status','price'] 

class UnftUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unft
        fields = ['status','price']        
