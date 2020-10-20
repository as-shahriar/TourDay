from django.shortcuts import render


def map(request, username):
    return render(request, 'api/map.html', {'username': username})
