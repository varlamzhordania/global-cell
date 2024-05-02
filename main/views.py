from django.shortcuts import render, redirect


def home_view(request, *args, **kwargs):
    my_context = {
        "Title": "Welcome to global-cell",
    }
