from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.contrib import messages


@login_required
def profile_view(request):
    if request.user.is_superuser:
        # Для суперпользователя показываем специальный профиль
        return render(request, "main/profile_superuser.html")

    # Для обычных пользователей
    profile = request.user.profile

    if profile.role == "client":
        return render(request, "main/profile_client.html")
    elif profile.role == "employee":
        return render(request, "main/profile_employee.html")

    return redirect("home")


@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Сохраняем только поля, соответствующие роли пользователя
            profile = form.save(commit=False)

            # Если пользователь - суперадминистратор, сохраняем все поля
            if request.user.is_superuser:
                profile.save()
            # Если пользователь - клиент, сохраняем только поля клиента
            elif profile.role == "client":
                # Сохраняем только поля клиента
                profile.company_name = form.cleaned_data['company_name']
                profile.contact_person = form.cleaned_data['contact_person']
                profile.address = form.cleaned_data['address']
                profile.phone = form.cleaned_data['phone']
                profile.save()
            # Если пользователь - сотрудник, сохраняем только поля сотрудника
            elif profile.role == "employee":
                # Сохраняем только поля сотрудника
                profile.position = form.cleaned_data['position']
                profile.department = form.cleaned_data['department']
                profile.birth_date = form.cleaned_data['birth_date']
                profile.work_phone = form.cleaned_data['work_phone']
                profile.home_phone = form.cleaned_data['home_phone']
                profile.save()

            messages.success(request, "Профиль обновлён.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    # Определяем, какой шаблон использовать в зависимости от роли
    if request.user.is_superuser:
        template = "main/profile_edit_superuser.html"
    elif profile.role == "client":
        template = "main/profile_edit_client.html"
    else:
        template = "main/profile_edit_employee.html"

    return render(request, template, {"form": form})
