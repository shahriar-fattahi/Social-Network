from django.db.models import Q
from django.utils import timezone
from django_filters import CharFilter, FilterSet
from rest_framework.exceptions import APIException

from .models import Post


class PostFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    auther__in = CharFilter(method="filter_author__in")
    created_at__range = CharFilter(method="filter_created_at__range")

    def filter_author__in(self, queryset, name, value):
        authers = value.split(",")
        if len(authers) > 10:
            raise APIException("You cannot add more than 10 emails.")

        return queryset.filter(auther__email__in=authers)

    def filter_created_at__range(self, queryset, name, value):
        range = value.split(",")
        if len(range) > 2:
            raise APIException("post create time range must be less than two time.")
        start, end = range

        if not end:
            end = timezone.now()
        if not start:
            return queryset.filter(created_at__lte=end)
        return queryset.filter(
            Q(created_at__date__gte=start) & Q(created_at__date__lte=end)
        )

    class Meta:
        model = Post
        fields = [
            "title",
        ]
