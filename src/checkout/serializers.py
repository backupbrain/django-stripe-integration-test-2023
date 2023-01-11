from rest_framework import serializers

class StripeResponseSerializer(serializers.Serializer):
    """Stripe response serializer."""

    status = serializers.CharField(max_length=200)
