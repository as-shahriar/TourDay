from django.shortcuts import render

# Create your views here.
def search(request):
    return render(request,'blog/search.html')

def home(request):
    return render(request,'blog/home.html')

def details(request):
    return render(request,'blog/details.html')