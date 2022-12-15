from django.forms import ModelForm
from .models import *

class ItemUpdateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['amount']
class ChangeCategoryForm(ModelForm):
    class Meta:
        model = Item
        fields = ['category_name']

class ItemCreateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category_name', 'amount']