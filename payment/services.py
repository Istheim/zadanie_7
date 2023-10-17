import stripe
from django.conf import settings


def create_payment(self):
    stripe.api_key = settings.STRIPE_PUBLIC_KEY
    intent = stripe.PaymentIntent.create(
        amount=2000,
        currency="usd",
        automatic_payment_methods={"enabled": True},
    )
    return intent
