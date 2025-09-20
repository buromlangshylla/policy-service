from django.utils.timezone import now


def generate_policy_number():
    year = now().year
    from .models import Policy
    count = Policy.objects.count() + 1
    return f"POL-{year}-{count:05d}"