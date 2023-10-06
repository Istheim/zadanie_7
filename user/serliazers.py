from rest_framework import serializers

from payment.serliazers import PaymentSerializer
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='payment_set', many=True)  # Сериализатор для истории платежей

    class Meta:
        model = User
        fields = '__all__'
