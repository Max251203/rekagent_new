from django import forms
from .models import Profile, Position, Department, Service, Order, PaymentOrder
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': 'new-password', 'id': 'id_password'})
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': 'new-password', 'id': 'id_password2'})
    )
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label='Роль',
                             widget=forms.Select(attrs={'class': 'form-control'}))

    # Поля для клиента
    company_name = forms.CharField(
        label='Название компании',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact_person = forms.CharField(
        label='Контактное лицо',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label='Адрес',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label='Телефон',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Поля для сотрудника
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        label='Должность',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label='Отдел',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    birth_date = forms.DateField(
        label='Дата рождения',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    work_phone = forms.CharField(
        label='Рабочий телефон',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    home_phone = forms.CharField(
        label='Домашний телефон',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'value': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'value': ''}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValidationError("Введите корректный email адрес.")
            return email

        def clean_password(self):
            password = self.cleaned_data.get('password')
            if len(password) < 8:
                raise ValidationError(
                    "Пароль должен быть не менее 8 символов.")
            if not re.search(r'\d', password):
                raise ValidationError(
                    "Пароль должен содержать хотя бы одну цифру.")
            if not re.search(r'[A-Za-z]', password):
                raise ValidationError(
                    "Пароль должен содержать хотя бы одну букву.")
            if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
                raise ValidationError(
                    "Пароль должен содержать хотя бы один спецсимвол.")
            return password

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            password2 = cleaned_data.get("password2")
            if password and password2 and password != password2:
                self.add_error('password2', "Пароли не совпадают")

            role = cleaned_data.get('role')

            # Проверка обязательных полей для клиента
            if role == 'client':
                company_name = cleaned_data.get('company_name')
                contact_person = cleaned_data.get('contact_person')
                phone = cleaned_data.get('phone')

                if not company_name:
                    self.add_error(
                        'company_name', "Это поле обязательно для клиента")
                if not contact_person:
                    self.add_error('contact_person',
                                   "Это поле обязательно для клиента")
                if not phone:
                    self.add_error('phone', "Это поле обязательно для клиента")

            # Проверка обязательных полей для сотрудника
            elif role == 'employee':
                position = cleaned_data.get('position')
                department = cleaned_data.get('department')
                birth_date = cleaned_data.get('birth_date')

                if not position:
                    self.add_error(
                        'position', "Это поле обязательно для сотрудника")
                if not department:
                    self.add_error(
                        'department', "Это поле обязательно для сотрудника")
                if not birth_date:
                    self.add_error(
                        'birth_date', "Это поле обязательно для сотрудника")

            return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'company_name', 'contact_person', 'address', 'phone',
                  'position', 'department', 'birth_date', 'work_phone', 'home_phone']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'work_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'home_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'salary']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'head', 'employee_count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'head': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'unit', 'material']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['employee', 'client', 'service', 'date_received',
                  'quantity', 'date_executed', 'discount']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'date_received': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'date_executed': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем пользователей по ролям
        self.fields['employee'].queryset = User.objects.filter(
            profile__role='employee')
        self.fields['client'].queryset = User.objects.filter(
            profile__role='client')


class PaymentOrderForm(forms.ModelForm):
    class Meta:
        model = PaymentOrder
        fields = ['order', 'date_paid']
        widgets = {
            'order': forms.Select(attrs={'class': 'form-control'}),
            'date_paid': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Оставьте пустым, если не хотите менять пароль'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'is_active', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
