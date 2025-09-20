import uuid
from django.db import models
from django.utils import timezone

from policies.utils import generate_policy_number


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Policy(TimeStampedModel):
    STATUS_CHOICES = [
        ("active","Active"), ("lapsed","Lapsed"),
        ("cancelled","Cancelled"), ("expired","Expired")
    ]
    UNDERWRITING_CHOICES = [("pending","Pending"),("approved","Approved"),("rejected","Rejected")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    policy_number = models.CharField(max_length=64, unique=True, null=True, blank=True)
    customer_id = models.UUIDField()  # no DB FK — resolved via Customer service
    product_code = models.CharField(max_length=50)
    coverage_amount = models.DecimalField(max_digits=14, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_frequency = models.CharField(max_length=20, default="annual")  # monthly/annual...
    start_date = models.DateField()
    end_date = models.DateField()
    term_years = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    underwriting_status = models.CharField(max_length=20, choices=UNDERWRITING_CHOICES, default="pending")
    agent_id = models.UUIDField(null=True, blank=True)
    add_ons = models.JSONField(null=True, blank=True)
    nominees = models.JSONField(null=True, blank=True)
    next_premium_due_date = models.DateField(null=True, blank=True)
    grace_period_end_date = models.DateField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(fields=["policy_number"]),
            models.Index(fields=["customer_id"]),
            models.Index(fields=["status"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.policy_number

    def save(self, *args, **kwargs):
        if not self.policy_number:
            self.policy_number = generate_policy_number()
        super().save(*args, **kwargs)


class PremiumPayment(TimeStampedModel):
    STATUS = [("pending","Pending"),("success","Success"),("failed","Failed")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="payments")
    paid_at = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    transaction_ref = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="success")
