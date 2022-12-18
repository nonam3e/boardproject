from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class Item(models.Model):
    category_name = models.ForeignKey(Category, on_delete = models.SET_DEFAULT, default=1)
    name = models.CharField(max_length = 150, unique=True)
    amount = models.PositiveIntegerField(default=0)
    last_changed = models.DateTimeField(auto_now=True)
    last_changer = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name