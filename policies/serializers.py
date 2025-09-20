import requests
from decouple import config
from rest_framework import serializers
from .models import Policy, PremiumPayment


CUSTOMER_SERVICE_URL = config("CUSTOMER_SERVICE_URL", default="http://localhost:8001")
AGENT_SERVICE_URL = config("AGENT_SERVICE_URL", default="http://localhost:8002")


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

    def validate_customer_id(self, value):
        url = f"{CUSTOMER_SERVICE_URL}/customers/{value}/"
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code != 200:
                raise serializers.ValidationError("Invalid customer_id: customer does not exist")
        except requests.exceptions.RequestException:
            raise serializers.ValidationError("Customer Service unavailable")
        return value

    def validate_agent_id(self, value):
        if value is None:
            return value
        url = f"{AGENT_SERVICE_URL}/auth/user/{int(value)}/"
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code != 200:
                raise serializers.ValidationError("Invalid agent_id: agent does not exist")
        except requests.exceptions.RequestException:
            raise serializers.ValidationError("Agent Service unavailable")
        return value

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError({
                "start_date": "start_date must be smaller than end_date."
            })
        return attrs
