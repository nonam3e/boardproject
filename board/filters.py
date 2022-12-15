import django_filters
from board.models import Item, Category


class ItemFilter(django_filters.FilterSet):
    amount = django_filters.RangeFilter()
    last_changed = django_filters.DateTimeFromToRangeFilter()
    o = django_filters.OrderingFilter(
    fields= ['name', 'category_name', 'amount', 'last_changed'],
    field_labels={
            'category_name': 'Category',
            'amount': 'Quantity',
            'last_changed': 'Last Modified',
        }
)
    # amount__gt = django_filters.NumberFilter(field_name='amount', lookup_expr='gt')
    # amount__lt = django_filters.NumberFilter(field_name='amount', lookup_expr='lt')
    # changed_date = django_filters.NumberFilter(field_name='last_changed', lookup_expr='date')
    # release_year__gt = django_filters.NumberFilter(field_name='last_changed', lookup_expr='date__gt')
    # release_year__lt = django_filters.NumberFilter(field_name='last_changed', lookup_expr='date__lt')
    class Meta:
        model = Item
        fields = ['name', 'category_name', 'amount', 'last_changed']
        # fields = {
        #     'name': ['exact','gt','lt'], 
        #     'amount': ['exact','gt','lt'], 
        #     'last_changed': ['exact','gt', 'lt']}

class CategoryFilter(django_filters.FilterSet):
    class Meta: 
        model = Category
        fields = ['name']