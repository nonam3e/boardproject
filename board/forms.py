from django.forms import ModelForm
from .models import *

class ItemUpdateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['id','amount']
