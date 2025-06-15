from django.contrib import admin
from .models import (
    Position,
    Department,
    Service,
    Order,
    PaymentOrder,
    Profile,
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "salary")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "head", "employee_count")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "company_name", "position", "department")
    list_filter = ("role",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "unit", "material")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("client", "service", "employee",
                    "date_received", "date_executed", "quantity", "discount")


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "date_paid")
