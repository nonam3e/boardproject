from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

CREATION = 1
CHANGE = 2
DELETION = 3
REPLACEMENT = 4

ACTION_FLAG_CHOICES = (
    (CREATION, _("Creation")),
    (CHANGE, _("Change")),
    (DELETION, _("Deletion")),
    (REPLACEMENT, _("Replacement")),
)

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
    
    def __str__(self):
        return self.name

class Logs(models.Model):
    action_time = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField(choices=ACTION_FLAG_CHOICES)