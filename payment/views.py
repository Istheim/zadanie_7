from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from payment.filters import PaymentFilter
from payment.models import Payment
from payment.serliazers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PaymentFilter