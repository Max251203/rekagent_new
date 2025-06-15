from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Position
from .forms import PositionForm
from django.contrib import messages


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
@user_passes_test(is_staff_or_admin)
def position_list(request):
    positions = Position.objects.all()
    return render(request, 'main/positions/list.html', {'positions': positions})


@login_required
@user_passes_test(is_staff_or_admin)
def position_create(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Должность успешно создана")
            return redirect('position_list')
    else:
        form = PositionForm()
    return render(request, 'main/positions/form.html', {'form': form, 'title': 'Добавить должность'})


@login_required
@user_passes_test(is_staff_or_admin)
def position_update(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, "Должность успешно обновлена")
            return redirect('position_list')
    else:
        form = PositionForm(instance=position)
    return render(request, 'main/positions/form.html', {'form': form, 'title': 'Редактировать должность'})


@login_required
@user_passes_test(is_staff_or_admin)
def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        position.delete()
        messages.success(request, "Должность успешно удалена")
        return redirect('position_list')
    return render(request, 'main/positions/confirm_delete.html', {'position': position})
