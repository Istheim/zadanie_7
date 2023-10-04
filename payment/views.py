from rest_framework import viewsets

from payment.models import Payment
from payment.serliazers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()