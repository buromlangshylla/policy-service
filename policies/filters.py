import django_filters
from .models import Policy


class PolicyFilter(django_filters.FilterSet):
    start_date = django_filters.DateFromToRangeFilter()
    end_date = django_filters.DateFromToRangeFilter()
    grace_period_end_date = django_filters.DateFromToRangeFilter()
    status = django_filters.CharFilter(lookup_expr="iexact")
    agent_id = django_filters.UUIDFilter()

    class Meta:
        model = Policy
        fields = ["status", "start_date", "end_date", "grace_period_end_date", "agent_id"]

