from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import PaymentOrder
from .forms import PaymentOrderForm
from django.contrib import messages
from decimal import Decimal


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
def payment_list(request):
    # Если сотрудник или админ - показываем все платежи
    if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'employee'):
        payments = PaymentOrder.objects.select_related(
            'order', 'order__client', 'order__service').all()
    # Если клиент - показываем только его платежи
    elif hasattr(request.user, 'profile') and request.user.profile.role == 'client':
        payments = PaymentOrder.objects.select_related('order', 'order__client', 'order__service').filter(
            order__client=request.user
        )
    else:
        payments = PaymentOrder.objects.none()

    # Расчет итоговой суммы для каждого платежа
    for payment in payments:
        order = payment.order
        if order and order.service and order.service.price:
            price = order.service.price
            quantity = order.quantity or 0
            discount = Decimal(order.discount or 0) / Decimal(100)
            payment.total = price * quantity * (1 - discount)
        else:
            payment.total = Decimal('0.00')

    return render(request, 'main/payments/list.html', {'payments': payments})


@login_required
@user_passes_test(is_staff_or_admin)
def payment_create(request):
    if request.method == 'POST':
        form = PaymentOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Платеж успешно создан")
            return redirect('payment_list')
    else:
        form = PaymentOrderForm()
    return render(request, 'main/payments/form.html', {'form': form, 'title': 'Добавить платёж'})


@login_required
@user_passes_test(is_staff_or_admin)
def payment_update(request, pk):
    payment = get_object_or_404(PaymentOrder, pk=pk)
    if request.method == 'POST':
        form = PaymentOrderForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, "Платеж успешно обновлен")
            return redirect('payment_list')
    else:
        form = PaymentOrderForm(instance=payment)
    return render(request, 'main/payments/form.html', {'form': form, 'title': 'Редактировать платёж'})


@login_required
@user_passes_test(is_staff_or_admin)
def payment_delete(request, pk):
    payment = get_object_or_404(PaymentOrder, pk=pk)
    if request.method == 'POST':
        payment.delete()
        messages.success(request, "Платеж успешно удален")
        return redirect('payment_list')
    return render(request, 'main/payments/confirm_delete.html', {'payment': payment})
