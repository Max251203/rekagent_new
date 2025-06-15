from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order
from .forms import OrderForm
from django.contrib import messages
from decimal import Decimal


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
def order_list(request):
    # Если сотрудник или админ - показываем все заказы
    if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'employee'):
        orders = Order.objects.select_related(
            'client', 'employee', 'service').all()
    # Если клиент - показываем только его заказы
    elif hasattr(request.user, 'profile') and request.user.profile.role == 'client':
        orders = Order.objects.select_related('client', 'employee', 'service').filter(
            client=request.user
        )
    else:
        orders = Order.objects.none()

    # Расчет итоговой суммы для каждого заказа
    for order in orders:
        if order.service and order.service.price:
            price = order.service.price
            quantity = order.quantity or 0
            discount = Decimal(order.discount or 0) / Decimal(100)
            order.total = price * quantity * (1 - discount)
        else:
            order.total = Decimal('0.00')

    return render(request, 'main/orders/list.html', {'orders': orders})


@login_required
@user_passes_test(is_staff_or_admin)
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заказ успешно создан")
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'main/orders/form.html', {'form': form, 'title': 'Добавить заказ'})


@login_required
@user_passes_test(is_staff_or_admin)
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Заказ успешно обновлен")
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'main/orders/form.html', {'form': form, 'title': 'Редактировать заказ'})


@login_required
@user_passes_test(is_staff_or_admin)
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Заказ успешно удален")
        return redirect('order_list')
    return render(request, 'main/orders/confirm_delete.html', {'order': order})
