from rest_framework import serializers
from deal.models import Deal


class DealSerializer(serializers.ModelSerializer):
    from_user_username = serializers.ReadOnlyField(source='from_user.username')
    to_user_username = serializers.ReadOnlyField(source='to_user.username')
    class Meta:
        model = Deal
        fields = [
            'id',
            'unft',
            'from_user',
            'from_user_username',
            'to_user_username',
            'price',
            'status',
            'created_at',
            'updated_at'
            ]
        write_only_fields = ['from_user']

class DealUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ['status']
        write_only_fields = ['status']