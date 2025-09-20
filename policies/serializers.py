from rest_framework import serializers
from .models import Policy, PremiumPayment


class PremiumPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPayment
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class PolicySerializer(serializers.ModelSerializer):
    payments = PremiumPaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Policy
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "version"]
