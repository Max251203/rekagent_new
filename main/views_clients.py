from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
@user_passes_test(is_staff_or_admin)
def client_list(request):
    search_query = request.GET.get("q")

    clients = User.objects.filter(profile__role='client')
    if search_query:
        clients = clients.filter(
            Q(profile__company_name__icontains=search_query) |
            Q(profile__contact_person__icontains=search_query) |
            Q(profile__phone__icontains=search_query)
        )

    context = {'clients': clients}
    return render(request, 'main/clients/list.html', context)
