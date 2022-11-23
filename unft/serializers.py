from rest_framework import serializers
from .models import Unft

class UnftSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    
    def get_creator(self, obj):
        return obj.creator.username
    def get_owner(self, obj):
        return obj.owner.username

    class Meta :
        model = Unft
        fields = "__all__"
