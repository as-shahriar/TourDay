from django.shortcuts import render


def loginView(request):
    return render(request, "_auth/login.html")
