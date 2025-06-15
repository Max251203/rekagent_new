from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Order, Service, PaymentOrder
from decimal import Decimal


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
@user_passes_test(is_staff_or_admin)
def reports(request):
    # Пример: список клиентов с суммой заказов и оплат
    clients = User.objects.filter(profile__role='client')
    client_stats = []
    for client in clients:
        orders = Order.objects.filter(client=client)
        total_orders = orders.count()
        total_sum = Decimal('0.00')
        for order in orders:
            if order.service and order.service.price:
                price = order.service.price
                quantity = order.quantity or 0
                discount = Decimal(order.discount or 0) / Decimal(100)
                order_sum = price * quantity * (1 - discount)
                total_sum += order_sum

        payments = PaymentOrder.objects.filter(order__client=client)
        total_payments = payments.count()
        client_stats.append({
            'client': client,
            'total_orders': total_orders,
            'total_sum': total_sum,
            'total_payments': total_payments,
        })

    # Пример: рейтинг услуг
    service_stats = []
    for service in Service.objects.all():
        count = Order.objects.filter(service=service).count()
        service_stats.append({'service': service, 'count': count})

    # Заказы с расчетом оплаты
    # Ограничиваем 20 последними заказами
    orders = Order.objects.all().order_by('-date_received')[:20]

    # Расчет итоговой суммы для каждого заказа
    for order in orders:
        if order.service and order.service.price:
            price = order.service.price
            quantity = order.quantity or 0
            discount = Decimal(order.discount or 0) / Decimal(100)
            order.total = price * quantity * (1 - discount)
        else:
            order.total = Decimal('0.00')

    return render(request, 'main/reports/index.html', {
        'client_stats': client_stats,
        'service_stats': service_stats,
        'orders': orders,
    })
