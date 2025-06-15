from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Создаем пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Обновляем профиль
            profile = user.profile
            profile.role = form.cleaned_data['role']

            # Заполняем поля в зависимости от роли
            if profile.role == 'client':
                profile.company_name = form.cleaned_data['company_name']
                profile.contact_person = form.cleaned_data['contact_person']
                profile.address = form.cleaned_data['address']
                profile.phone = form.cleaned_data['phone']
            elif profile.role == 'employee':
                profile.position = form.cleaned_data['position']
                profile.department = form.cleaned_data['department']
                profile.birth_date = form.cleaned_data['birth_date']
                profile.work_phone = form.cleaned_data['work_phone']
                profile.home_phone = form.cleaned_data['home_phone']

            profile.save()

            # Авторизуем пользователя
            user = authenticate(username=user.username,
                                password=form.cleaned_data['password'])
            login(request, user)
            messages.success(request, "Регистрация успешно завершена!")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})
