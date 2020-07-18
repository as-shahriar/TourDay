from django.shortcuts import render
from blog.forms import blogPostForm

# Create your views here.
def search(request):
    return render(request,'blog/search.html')

def home(request):
    return render(request,'blog/home.html')

def details(request):
    return render(request,'blog/details.html')

def addPost(request):
    if request.method == 'POST':
        form = blogPostForm(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.save()
    else:
        form = blogPostForm()
    return render(request,'blog/add_post.html', {'form':form})
