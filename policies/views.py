from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Policy, PremiumPayment
from .permissions import IsJWTAuthenticated
from .serializers import PolicySerializer, PremiumPaymentSerializer


class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsJWTAuthenticated, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["policy_number", "product_code", "status"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=["get"], url_path="by-customer/(?P<customer_id>[^/.]+)")
    def list_by_customer(self, request, customer_id=None):
        qs = self.queryset.filter(customer_id=customer_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class PremiumPaymentViewSet(viewsets.ModelViewSet):
    queryset = PremiumPayment.objects.all()
    serializer_class = PremiumPaymentSerializer
    permission_classes = [IsJWTAuthenticated, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["transaction_ref", "status"]
