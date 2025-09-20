# policy/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PolicyViewSet, PremiumPaymentViewSet

router = SimpleRouter()
router.register(r"", PolicyViewSet, basename="policies")
# router.register(r"payments", PremiumPaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]
