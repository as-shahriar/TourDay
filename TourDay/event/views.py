from django.shortcuts import render


def dashboard(request):
    return render(request, 'event/dashboard.html')


def eventView(request, id):
    return render(request, 'event/event.html')
