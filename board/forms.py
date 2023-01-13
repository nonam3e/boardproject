from django.forms import ModelForm
from django import forms
from .models import *

class ItemUpdateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['amount']
class ItemRemoveForm(ModelForm):
    class Meta:
        model = Item
        fields = ['id','amount']
    # def clean(self):
    #     form_data = self.cleaned_data
    #     if form_data['amount'] > Item.objects.get(id = form_data['id']):
    #         raise ValueError('Input amount is greater than in total')
    #     return form_data        

class ChangeCategoryForm(ModelForm):
    class Meta:
        model = Item
        fields = ['id','category_name', 'amount']

class ItemCreateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category_name', 'amount']