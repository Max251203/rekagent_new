from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User

# ========== Роли пользователей ==========


class Profile(models.Model):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('employee', 'Сотрудник'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Поля для клиента
    company_name = models.CharField(
        "Название компании", max_length=100, null=True, blank=True)
    contact_person = models.CharField(
        "Контактное лицо", max_length=100, null=True, blank=True)
    address = models.CharField("Адрес", max_length=200, null=True, blank=True)
    phone = models.CharField("Телефон", max_length=20, null=True, blank=True)

    # Поля для сотрудника
    position = models.ForeignKey(
        'Position', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Должность")
    department = models.ForeignKey(
        'Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Отдел")
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    work_phone = models.CharField(
        "Рабочий телефон", max_length=20, null=True, blank=True)
    home_phone = models.CharField(
        "Домашний телефон", max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

# ========== Таблицы: Должность, Отдел, Услуга, Заказ, Платёж ==========


class Position(models.Model):
    name = models.CharField("Название должности", max_length=50)
    salary = models.DecimalField(
        "Оклад", max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField("Название отдела", max_length=30)
    head = models.CharField("Начальник", max_length=50, null=True, blank=True)
    employee_count = models.PositiveIntegerField(
        "Количество сотрудников", null=True, blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField("Наименование", max_length=50)
    price = models.DecimalField(
        "Цена", max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField("Единица измерения",
                            max_length=30, null=True, blank=True)
    material = models.CharField(
        "Материал", max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='employee_orders')
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='client_orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_received = models.DateField("Дата принятия заказа")
    quantity = models.PositiveIntegerField("Количество")
    date_executed = models.DateField(
        "Дата выполнения заказа", null=True, blank=True)
    discount = models.PositiveIntegerField(
        "Скидка", null=True, blank=True)  # в %

    def __str__(self):
        return f"Заказ #{self.id} для {self.client.profile.company_name}"


class PaymentOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_paid = models.DateField("Дата оплаты")

    def __str__(self):
        return f"Платёж №{self.id} (заказ {self.order.id})"


# ========== Сигналы для профиля ==========

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
