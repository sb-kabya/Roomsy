from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

User = get_user_model()


class UserRegistrationSerializer(BaseUserCreateSerializer):
    re_password = serializers.CharField(write_only=True)
    class Meta(BaseUserCreateSerializer.Meta):
        model  = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',
                  'phone_number', 'password', 're_password']
        extra_kwargs = {
            'first_name':  {'required': True},
            'last_name':   {'required': True},
            'password':    {'write_only': True},
            're_password': {'write_only': True},
        }
class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    re_password = serializers.CharField(write_only=True)
    class Meta:
        model  = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',
                  'full_name', 'balance', 'phone_number', 'is_email_verified', 'date_joined', 're_password']
        read_only_fields = ['id', 'email', 'balance', 'is_email_verified', 'date_joined']


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('1'),
        help_text='Amount to deposit (minimum $1)'
    )
