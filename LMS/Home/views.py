from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
@allowed_users(allowed_roles=['admin'])
def registerpage(request):
    form = CreateUserForm

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='staff')
            user.groups.add(group)

            messages.success(request, "Account was created for " + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            group = Group.objects.get(user=user)

            if str(group) == 'staff':
                return redirect('staff_home')

            elif str(group) == 'admin':
                return redirect('admin_home')

            else:
                return redirect('home')

        else:
            messages.info(request, "Username Or Password is Incorrect")

    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    return redirect('home')


def home(request):
    context = {}
    return render(request, 'home.html', context)


@unauthenticated_user
@allowed_users(allowed_roles=['staff'])
def staff_home(request):
    context = {}
    return render(request, 'staff_home.html', context)


@unauthenticated_user
@allowed_users(allowed_roles=['admin'])
def admin_home(request):
    context = {}
    return render(request, 'admin_home.html', context)