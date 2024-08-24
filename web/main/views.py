from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.db import IntegrityError

from core.utils import fancy_message
from accounts.forms import UserForm, PasswordChangeForm
from settings.models import Page, Slide

from .models import Device, Country, PaymentMethod
from .forms import DeviceForm, PaymentMethodForm


def home_view(request, *args, **kwargs):
    page_data = cache.get("home_page")

    supported_countries = Country.objects.filter(is_supported=True)

    if page_data is not None:
        page = page_data
    else:
        page = Page.objects.filter(type=Page.TypeChoices.HOME).first()
        cache.set('home_page', page, 900)

    my_context = {
        "Title": _("Welcome To Global Cell"),
        "page": page,
        "countries": supported_countries
    }
    return render(request, "pages/main/home.html", my_context)


@login_required
def dashboard_view(request, *args, **kwargs):
    slides = Slide.objects.filter(is_active=True)

    my_context = {
        "Title": _("Dashboard"),
        "slides": slides,
    }
    return render(request, "pages/dashboard/main.html", my_context)


@login_required
def phones_create(request, *args, **kwargs):
    if request.method == "POST":
        form = DeviceForm(request.POST, request.FILES)
        if form.is_valid():
            device = form.save(commit=False)
            device.user = request.user

            try:
                device.save()
                fancy_message(request, _(f"Device {device.sim_number} was added successfully"), level="success")
                return redirect("main:phones_list")
            except IntegrityError:
                fancy_message(
                    request,
                    _("You already have an active device with this phone number, try another."),
                    level="error"
                )
        else:
            fancy_message(request, _("Please make sure you have filled the form correctly"), level="error")

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
    is_verified = request.GET.get("is_verified", None)
    is_unlimited_minutes = request.GET.get("is_unlimited_minutes", None)
    plan_payment = request.GET.get("plan_payment", None)
    is_active = request.GET.get("is_active", None)

    queryset = Device.objects.filter(user=request.user)

    if search is not None:
        queryset = queryset.filter(sim_number__icontains=search)
    if is_verified is not None:
        queryset = queryset.filter(is_verified=is_verified)
    if is_unlimited_minutes is not None:
        queryset = queryset.filter(is_unlimited_minutes=is_unlimited_minutes)
    if plan_payment is not None:
        queryset = queryset.filter(plan_payment=plan_payment)
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    paginator = Paginator(queryset, 10)

    try:
        devices = paginator.page(page)
    except PageNotAnInteger:
        devices = paginator.page(1)
    except EmptyPage:
        devices = paginator.page(paginator.num_pages)

    my_context = {
        "Title": _("Phones List"),
        "queryset": devices,
        "page": page,
        "search": search,
        "is_verified": is_verified,
        "is_unlimited_minutes": is_unlimited_minutes,
        "plan_payment": plan_payment,
        "is_active": is_active,

    }

    return render(request, "pages/dashboard/phones_list.html", my_context)


@login_required
def financial_view(request, *args, **kwargs):
    if request.method == "POST":
        pm_id = request.POST.get("pm-id", None)
        if pm_id:
            pm_obj = get_object_or_404(PaymentMethod, pk=pm_id, user=request.user)
            data = {
                "id": pm_obj.id,
                "account_name": pm_obj.account_name,
                "account_number": pm_obj.account_number,
                "bank_name": pm_obj.bank_name,
                "swift_number": request.POST.get("swift_number", None),
                "iban_number": request.POST.get("iban_number", None),
            }
            form = PaymentMethodForm(instance=pm_obj, data=data)
            success_message = _("Bank Account {bank_name} updated successfully")
        else:
            form = PaymentMethodForm(request.POST)
            success_message = _("Bank Account {bank_name} was added successfully")

        if form.is_valid():
            payment = form.save(commit=False)
            if not pm_id:
                payment.user = request.user
            payment.save()
            fancy_message(request, success_message.format(bank_name=payment.bank_name), level="success")
            return redirect("main:financial")
        else:
            fancy_message(request, _("Please make sure you have filled the form correctly"), level="error")
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
def delete_payment_method_view(request, pk, *args, **kwargs):
    queryset = get_object_or_404(PaymentMethod, pk=pk, user=request.user)
    queryset.delete()
    fancy_message(request, _(f"Bank Account {queryset.bank_name} was deleted successfully"), level="success")
    return redirect("main:financial")


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
