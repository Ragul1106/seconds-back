import django_filters
from django.db.models import Q
from .models import BuyBike

class BikeFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    year_min = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    year_max = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    km_max = django_filters.NumberFilter(field_name="kilometers", lookup_expr="lte")
    engine_cc_min = django_filters.NumberFilter(field_name="engine_cc", lookup_expr="gte")
    engine_cc_max = django_filters.NumberFilter(field_name="engine_cc", lookup_expr="lte")

    # For textual filters, use icontains for partial matching (more user friendly)
    brand = django_filters.CharFilter(field_name="brand", lookup_expr="icontains")
    category = django_filters.CharFilter(field_name="category", lookup_expr="icontains")
    fuel_type = django_filters.CharFilter(field_name="fuel_type", lookup_expr="icontains")
    color = django_filters.CharFilter(field_name="color", lookup_expr="icontains")

    # custom multi-field search (search across title/description/brand/location.name)
    search = django_filters.CharFilter(method="search_filter")

    class Meta:
        model = BuyBike
        # keep fields empty so only our custom filters are exposed
        fields = []

    def search_filter(self, queryset, name, value):
        # treat location as FK -> search location.name
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(brand__icontains=value) |
            Q(location__name__icontains=value)
        )
