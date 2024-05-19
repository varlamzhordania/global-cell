"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include, re_path
from django.conf import settings

from accounts.forms import StylesCustomSetPasswordForm, StylesCustomPasswordResetForm

from .views import set_language

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace="main")),
    path('', include('accounts.urls', namespace="accounts")),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="pages/main/password_reset.html",
            form_class=StylesCustomPasswordResetForm, ),
        name="reset_password"
    ),
    path(
        "reset_password_done/",
        auth_views.PasswordResetDoneView.as_view(template_name="pages/main/password_reset_done.html"),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="pages/main/password_reset_form.html",
            form_class=StylesCustomSetPasswordForm
        ),
        name="password_reset_confirm"
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name="pages/main/password_reset_complete.html"),
        name="password_reset_complete"
    ),
    re_path(r'^rosetta/', include('rosetta.urls')),
    path("setlang/", set_language, name="set_language"),
    path('hijack/', include('hijack.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
