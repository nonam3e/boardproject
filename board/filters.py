import django_filters
from board.models import Item, Category


class ItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Name",lookup_expr="contains")
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