from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegisterForm, ProfileUpdateForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully! You can now log in."
            )

            return redirect('login')
    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Welcome to Splitly!")
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')

    return redirect('dashboard')


from django.core.exceptions import PermissionDenied


@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    return redirect('member_dashboard')


@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    return render(request, 'accounts/admin_dashboard.html')


@login_required
def member_dashboard_view(request):
    if request.user.is_superuser:
        raise PermissionDenied

    return render(request, 'accounts/dashboard.html')


@login_required
def profile_view(request):
    return render(
        request,
        'accounts/profile.html'
    )


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully!"
            )

            return redirect('profile')
    else:
        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        'accounts/edit_profile.html',
        {'form': form}
    )
