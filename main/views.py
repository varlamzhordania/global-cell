from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext as _

from core.utils import fancy_message
from accounts.forms import UserForm, PasswordChangeForm

from .models import Device, Country, PaymentMethod
from .forms import DeviceForm, PaymentMethodForm


def home_view(request, *args, **kwargs):
    my_context = {
        "Title": _("Welcome To Global Cell"),
    }
    return render(request, "pages/main/home.html", my_context)


@login_required
def dashboard_view(request, *args, **kwargs):
    my_context = {
        "Title": _("Dashboard")
    }
    return render(request, "pages/dashboard/main.html", my_context)


@login_required
def phones_create(request, *args, **kwargs):
    if request.method == "POST":
        form = DeviceForm(request.POST, request.FILES)
        if form.is_valid():
            device = form.save(commit=False)
            device.user = request.user
            device.save()
            fancy_message(request, _(f"Device {device} was add successfully"), level="success")
            return redirect("main:phones")
        else:
            fancy_message(request, _(f"Please makesure your have fill the form correctly"), level="error")
    else:
        form = DeviceForm()

    countries = Country.objects.filter(is_supported=True)
    my_context = {
        "Title": _("Add Your New Phone"),
        "form": form,
        "countries": countries,
    }
    return render(request, "pages/dashboard/phones_create.html", my_context)


@login_required
def phones_list(request, *args, **kwargs):
    page = request.GET.get("page", 1)
    search = request.GET.get("search", None)

    queryset = Device.objects.filter(user=request.user)

    if search is not None:
        queryset = queryset.filter(sim_number__icontains=search)

    paginator = Paginator(queryset, 1)

    try:
        devices = paginator.page(page)
    except PageNotAnInteger:
        devices = paginator.page(1)
    except EmptyPage:
        devices = paginator.page(paginator.num_pages)

    my_context = {
        "Title": _("Phones List"),
        "queryset": devices,
        "search": search,
        "page": page,
    }

    return render(request, "pages/dashboard/phones_list.html", my_context)


def financial_view(request, *args, **kwargs):
    if request.method == "POST":
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            fancy_message(request, _(f"Bank Account {payment.bank_name} was added successfully"), level="success")
            return redirect("main:financial")
        else:
            fancy_message(request, _(f"Please makesure your have fill the form correctly"), level="error")
    else:
        form = PaymentMethodForm()
    queryset = PaymentMethod.objects.filter(user=request.user)
    my_context = {
        "Title": _("Manage your financial"),
        "queryset": queryset,
        "form": form,
    }
    return render(request, "pages/dashboard/financial.html", my_context)


@login_required
def settings_view(request, *args, **kwargs):
    user_form = UserForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    my_context = {
        "Title": _("Settings"),
        "user_form": user_form,
        "password_form": password_form,
    }
    return render(request, "pages/dashboard/settings.html", my_context)

