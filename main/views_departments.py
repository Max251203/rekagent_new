from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Department
from .forms import DepartmentForm
from django.contrib import messages


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
@user_passes_test(is_staff_or_admin)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'main/departments/list.html', {'departments': departments})


@login_required
@user_passes_test(is_staff_or_admin)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Отдел успешно создан")
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'main/departments/form.html', {'form': form, 'title': 'Добавить отдел'})


@login_required
@user_passes_test(is_staff_or_admin)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Отдел успешно обновлен")
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'main/departments/form.html', {'form': form, 'title': 'Редактировать отдел'})


@login_required
@user_passes_test(is_staff_or_admin)
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, "Отдел успешно удален")
        return redirect('department_list')
    return render(request, 'main/departments/confirm_delete.html', {'department': department})
