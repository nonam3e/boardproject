from django.db.models.signals import post_save
from django.dispatch import receiver
from board.models import Item
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

# @receiver(post_save, sender=Item)
# def change_logger(sender, instance, **kwargs):
#     if kwargs.get('created', False):
#         # LogEntry.objects.log_action(
#         #                 user_id=instance.last_changer.id,
#         #                 content_type_id=ContentType.objects.get_for_model(Item).pk,
#         #                 object_id=instance.id,
#         #                 object_repr=instance.name,
#         #                 action_flag=ADDITION,
#         #                 change_message=f"new item amount {instance.amount} placed in {instance.category_name}")
#     elif kwargs.get("update_fields") is not None:
#         if "category_name" in kwargs.get("update_fields"):
#             LogEntry.objects.log_action(
#                             user_id=instance.last_changer.id,
#                             content_type_id=ContentType.objects.get_for_model(Item).pk,
#                             object_id=instance.id,
#                             object_repr=instance.name,
#                             action_flag=CHANGE,
#                             change_message=f"replaced to {instance.category_name}")