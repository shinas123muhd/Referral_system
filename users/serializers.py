from rest_framework import serializers
from .models import User,Referral

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'referral_code','reffered_by','points']

class ReferralSerializer(serializers.ModelSerializer):
    referred_user_name = serializers.SerializerMethodField(source='referred_user')
    class Meta:
        model = Referral
        fields = ['referring_user', 'referred_user','referred_user_name', 'timestamp']
    def get_referred_user_name(self, obj):
        return obj.referred_user.name if obj.referred_user else None

