import django_filters
from board.models import Item, Category


class ItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Name")
    amount = django_filters.RangeFilter(label="Quantity")
    category_name = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label="Category")
    last_changed = django_filters.DateTimeFromToRangeFilter(label="Last Modified")
    o = django_filters.OrderingFilter(
        fields= ['name', 'category_name', 'amount', 'last_changed'],
        field_labels={
                'name': "Name",
                'category_name': 'Category',
                'amount': 'Quantity',
                'last_changed': 'Last Modified',
            }
    )
    class Meta:
        model = Item
        fields = ['name', 'category_name', 'amount', 'last_changed']

class TotalFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Name",lookup_expr="contains")
    total_amount = django_filters.RangeFilter(label="Quantity")
    o = django_filters.OrderingFilter(
        fields= ['name', 'total_amount', 'last_changed'],
        field_labels={
                'name': "Name",
                'total_amount': 'Quantity',
                'last_changed': 'Last Modified',
            }
    )