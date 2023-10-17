from builtins import *

import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response

from payment.filters import PaymentFilter
from payment.models import Payment
from payment.serliazers import PaymentSerializer
from payment.services import create_payment


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PaymentFilter

    def create(self, request, *args, **kwargs):
        amount = request.data.get('amount')
        currency = 'usd'

        try:
            intent = create_payment(amount, currency)

            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                stripe_payment_intent_id=intent.id,
                payment_method=request.data.get('payment_method'),
            )

            serializer = self.get_serializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)