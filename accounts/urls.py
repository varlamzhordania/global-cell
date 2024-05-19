from django.urls import path
from .views import login_view, register_view, logout_view, profile_view, change_password_view


app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path("change_password/", change_password_view, name="change_password"),


]
