from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _

from core.utils import fancy_message

from .forms import UserForm, PasswordChangeForm
from .decorators import unauthenticated_user


@unauthenticated_user
def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                fancy_message(request, _(f'Welcome {user}!'), level="success")
                return redirect('main:dashboard')
            else:
                fancy_message(request, _('Invalid email or password.'), level="error")
        else:
            fancy_message(request, _('Email and password is required.'), level="error")

    my_context = {
        "Title": _("Sign In")
    }
    return render(request, "pages/main/login.html", my_context)


@login_required
@require_POST
def profile_view(request, *args, **kwargs):
    form = UserForm(instance=request.user, data=request.POST, files=request.FILES)
    if form.is_valid():
        user = form.save()
        fancy_message(request, _('Your profile has been updated.'), level="success")
        return redirect('main:settings')
    else:
        fancy_message(request, form.errors, level="error")
        return redirect('main:settings')


@login_required
@require_POST
def change_password_view(request, *args, **kwargs):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        fancy_message(request, _(f"Your password has been successfully updated !"), level="success")
        return redirect("account:profile")
    else:
        fancy_message(request, form.errors, level="error")
        return redirect(request.META["HTTP_REFERER"])


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    fancy_message(request, _("You have been logged out."), level="info")
    return redirect("accounts:login")
