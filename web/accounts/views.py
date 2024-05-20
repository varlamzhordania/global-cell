from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.core.cache import cache

from core.utils import fancy_message
from settings.models import Page

from .forms import UserForm, PasswordChangeForm, CustomUserCreationForm
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

    page_data = cache.get("login_page")

    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type=Page.TypeChoices.SIGNIN).first()
        cache.set('login_page', page, 900)

    my_context = {
        "Title": _("Sign In"),
        "page": page
    }
    return render(request, "pages/main/login.html", my_context)


@unauthenticated_user
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            fancy_message(
                request,
                _('Congratulations! You have successfully registered your account.'),
                level="success"
            )
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    page_data = cache.get("register_page")

    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type=Page.TypeChoices.SIGNUP).first()
        cache.set('register_page', page, 900)

    my_context = {
        "Title": _("Sign Up"),
        "form": form,
        "page": page,
    }
    return render(request, "pages/main/register.html", my_context)


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
