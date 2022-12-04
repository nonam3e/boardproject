from django.shortcuts import render, redirect
from board.filters import ItemFilter
from django.contrib.auth.decorators import login_required
from board.models import Item, Category
from board.forms import ItemUpdateForm
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

# Create your views here.
@login_required
def home(request):
    items = Item.objects.all().order_by('-last_changed')
    item_filters = ItemFilter(request.GET, queryset = items)
    items = item_filters.qs
    addform = ItemUpdateForm(request.POST)
    removeform = ItemUpdateForm(request.POST)

    return render(request, 'board/index.html', {
        'items': items, 'item_filters': item_filters, 'addform': addform, 'removeform': removeform
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
            issued_item.save()
            
            LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ContentType.objects.get_for_model(Item).pk,
                        object_id=issued_item.id,
                        object_repr=issued_item.name,
                        action_flag=ADDITION,
                        change_message=f"added {added_quantity} item(s)")
            return redirect(request.META.get('HTTP_REFERER', '/home'))

@login_required
def remove_from_stock(request, pk):
    issued_item = Item.objects.get(id = pk)
    form = ItemUpdateForm(request.POST)

    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            added_quantity = int(request.POST['amount'])
            if added_quantity > issued_item.amount:
                return redirect(request.META.get('HTTP_REFERER', '/home'))
            issued_item.amount -= added_quantity
            issued_item.save()
            LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ContentType.objects.get_for_model(Item).pk,
                        object_id=issued_item.id,
                        object_repr=issued_item.name,
                        action_flag=DELETION,
                        change_message=f"removed {added_quantity} item(s)")
            return redirect(request.META.get('HTTP_REFERER', '/home'))
