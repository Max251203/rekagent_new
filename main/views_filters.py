from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order, PaymentOrder
from datetime import date, timedelta, datetime
from decimal import Decimal


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
@user_passes_test(is_staff_or_admin)
def orders_by_period(request):
    # Получаем параметры из запроса или устанавливаем значения по умолчанию
    try:
        start_date_str = request.GET.get('start_date')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = date.today() - timedelta(days=30)
    except (ValueError, TypeError):
        start_date = date.today() - timedelta(days=30)

    try:
        end_date_str = request.GET.get('end_date')
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = date.today()
    except (ValueError, TypeError):
        end_date = date.today()

    orders = Order.objects.filter(
        date_received__gte=start_date,
        date_received__lte=end_date
    ).order_by('-date_received')

    # Расчет итоговой суммы для каждого заказа
    total_sum = Decimal('0.00')
    for order in orders:
        if order.service and order.service.price:
            price = order.service.price
            quantity = order.quantity or 0
            discount = Decimal(order.discount or 0) / Decimal(100)
            order_total = price * quantity * (1 - discount)
            order.total = order_total
            total_sum += order_total
        else:
            order.total = Decimal('0.00')

    return render(request, 'main/filters/orders_by_period.html', {
        'orders': orders,
        'total_sum': total_sum,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
@user_passes_test(is_staff_or_admin)
def payments_by_period(request):
    # Получаем параметры из запроса или устанавливаем значения по умолчанию
    try:
        start_date_str = request.GET.get('start_date')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = date.today() - timedelta(days=30)
    except (ValueError, TypeError):
        start_date = date.today() - timedelta(days=30)

    try:
        end_date_str = request.GET.get('end_date')
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = date.today()
    except (ValueError, TypeError):
        end_date = date.today()

    payments = PaymentOrder.objects.filter(
        date_paid__gte=start_date,
        date_paid__lte=end_date
    ).order_by('-date_paid')

    # Расчет итоговой суммы для каждого платежа
    total_sum = Decimal('0.00')
    for payment in payments:
        order = payment.order
        if order and order.service and order.service.price:
            price = order.service.price
            quantity = order.quantity or 0
            discount = Decimal(order.discount or 0) / Decimal(100)
            payment_total = price * quantity * (1 - discount)
            payment.total = payment_total
            total_sum += payment_total
        else:
            payment.total = Decimal('0.00')

    return render(request, 'main/filters/payments_by_period.html', {
        'payments': payments,
        'total_sum': total_sum,
        'start_date': start_date,
        'end_date': end_date,
    })
