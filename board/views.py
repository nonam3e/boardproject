from django.shortcuts import render, redirect
from board.filters import ItemFilter, TotalFilter
from django.contrib.auth.decorators import login_required
from board.models import Item, Category
from board.forms import ItemUpdateForm, ItemCreateForm, ChangeCategoryForm, ItemRemoveForm
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, Max
from django.contrib import messages

# Create your views here.
@login_required
def home(request):
    items = Item.objects.all().order_by('-last_changed')
    item_filters = ItemFilter(request.GET, queryset = items)
    items = item_filters.qs
    addform = ItemUpdateForm(request.POST)
    removeform = ItemUpdateForm(request.POST)
    newform = ItemCreateForm(request.POST)
    categoryform = ChangeCategoryForm(request.POST)

    return render(request, 'board/index.html', {
        'items': items, 'item_filters': item_filters, 'addform': addform, 'removeform': removeform, 'newform': newform,
        'categoryform': categoryform,
    })
@login_required
def show_total(request):
    items = Item.objects.values('name').annotate(total_amount=Sum('amount')).annotate(last_changed=Max('last_changed')).order_by('-last_changed')
    item_filters = TotalFilter(request.GET, queryset=items)
    items = item_filters.qs
    return render(request, 'board/total.html', {
        'items': items, 'item_filters': item_filters
    })


@login_required
def changes(request):
    items = LogEntry.objects.all()
    return render(request, 'board/changes.html', {'items': items})
    

@login_required
def add_to_stock(request, pk):
    issued_item = Item.objects.get(id = pk)
    form = ItemUpdateForm(request.POST)

    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            added_quantity = int(request.POST['amount'])
            issued_item.amount += added_quantity
            issued_item.last_changer = request.user
            issued_item.save()
            
            LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ContentType.objects.get_for_model(Item).pk,
                        object_id=issued_item.id,
                        object_repr=issued_item.name,
                        action_flag=ADDITION,
                        change_message=f"added {added_quantity} item(s) to {issued_item.category_name.name}")
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_from_stock(request, pk):
    issued_item = Item.objects.get(id = pk)
    form = ItemRemoveForm(request.POST)

    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            added_quantity = int(request.POST['amount'])
            if added_quantity > issued_item.amount:
                messages.warning(request, 'Input quantity > existing quantity')
            else:
                issued_item.amount -= added_quantity
                issued_item.last_changer = request.user
                issued_item.save()
                LogEntry.objects.log_action(
                            user_id=request.user.id,
                            content_type_id=ContentType.objects.get_for_model(Item).pk,
                            object_id=issued_item.id,
                            object_repr=issued_item.name,
                            action_flag=DELETION,
                            change_message=f"removed {added_quantity} item(s) from {issued_item.category_name.name}")
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def new_item(request):
    form = ItemCreateForm(request.POST)

    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            issued_category = Category.objects.get(id = request.POST["category_name"])
            issued_item = Item.objects.create(name = request.POST["name"], category_name = issued_category, amount = request.POST["amount"], last_changer = request.user)
            issued_item.save(update_fields=[])
            LogEntry.objects.log_action(
                        user_id=issued_item.last_changer.id,
                        content_type_id=ContentType.objects.get_for_model(Item).pk,
                        object_id=issued_item.id,
                        object_repr=issued_item.name,
                        action_flag=ADDITION,
                        change_message=f"new item amount {issued_item.amount} placed in {issued_item.category_name}")
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def change_category(request, pk):
    if request.method == 'POST':
        print(request.POST)
        form = ChangeCategoryForm(request.POST)
        if form.is_valid():
            issued_item = Item.objects.get(id = pk)
            new_category = Category.objects.get(id = request.POST['category_name'])
            old_category = issued_item.category_name
            if int(request.POST['amount']) > issued_item.amount or issued_item.category_name == new_category:
                messages.warning(request, 'Input quantity > existing quantity')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            elif int(request.POST['amount']) == 0 or int(request.POST['amount']) == issued_item.amount:
                if Item.objects.filter(name=issued_item.name, category_name=new_category).exists():
                    new_item = Item.objects.get(name=issued_item.name, category_name=new_category)
                    new_item.amount += issued_item.amount
                    new_item.last_changer = request.user
                    issued_item.delete()
                    new_item.save()
                else:
                    issued_item.category_name = new_category
                    issued_item.last_changer = request.user
                    issued_item.save()
                LogEntry.objects.log_action(
                            user_id=issued_item.last_changer.id,
                            content_type_id=ContentType.objects.get_for_model(Item).pk,
                            object_id=issued_item.id,
                            object_repr=issued_item.name,
                            action_flag=CHANGE,
                            change_message=f"replaced all from {old_category} to {new_category}")
            else:
                new_item, created = Item.objects.get_or_create(name=issued_item.name, category_name=new_category, defaults={"amount": 0, "last_changer": request.user})
                new_item.amount += int(request.POST['amount'])
                new_item.last_changer = request.user
                issued_item.amount -= int(request.POST['amount'])
                issued_item.last_changer = request.user
                issued_item.save()
                new_item.save()
                LogEntry.objects.log_action(
                            user_id=issued_item.last_changer.id,
                            content_type_id=ContentType.objects.get_for_model(Item).pk,
                            object_id=issued_item.id,
                            object_repr=issued_item.name,
                            action_flag=CHANGE,
                            change_message=f"replaced {request.POST['amount']} from {old_category} to {new_category}")
            
        return redirect(request.META.get('HTTP_REFERER', '/'))