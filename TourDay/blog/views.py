from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import blogPostForm
from django.contrib.auth.decorators import login_required
from blog.models import blogPost
from django.core.paginator import Paginator
from django.db.models import Q




class division_post_count:
    def __init__(self):
        self.Rajshahi = blogPost.objects.filter(division='Rajshahi').count()
        self.Chittagong = blogPost.objects.filter(division='Chittagong').count()
        self.Dhaka = blogPost.objects.filter(division='Dhaka').count()
        self.Mymensingh = blogPost.objects.filter(division='Mymensingh').count()
        self.Khulna = blogPost.objects.filter(division='Khulna').count()
        self.Barishal = blogPost.objects.filter(division='Barishal').count()
        self.Rangpur = blogPost.objects.filter(division='Rangpur').count()
        self.Sylhet = blogPost.objects.filter(division='Sylhet').count()



 
# Create your views here.
def search(request):
    return render(request,'blog/search.html')


def home(request):

    if request.method == 'POST' and 'btn-search' in request.POST:
        q = request.POST.get('search').strip()
        if q:
            request.session['q'] = q
            return redirect('blog_search')

    # di_count = division_post_count()
   
    random_post = blogPost.objects.order_by('?')
    recent_post = blogPost.objects.order_by('-id')
    # print("Randomly post:  " + str(random_post.title))


    allpost = blogPost.objects.all().order_by('-id')
    paginator = Paginator(allpost, 5)  # Show 5 obj per page

    page = request.GET.get('page')
    allpost = paginator.get_page(page)

    context = {
        # # 'paginator_pages': paginator_pages,

        'di_count' : division_post_count(),
        'allpost' : allpost,
        'recent_post':recent_post,
        'random_post':random_post,
    }
    

    return render(request,'blog/home.html', context)

def details(request, id):
    if request.method == 'POST' and 'btn-search' in request.POST:
        q = request.POST.get('search').strip()
        if q:
            request.session['q'] = q
            return redirect('blog_search')

    # di_count = division_post_count() 

    details_obj = blogPost.objects.get(id = id)
    random_post = blogPost.objects.order_by('?')

    context = {
        'di_count' : division_post_count(),
        'details_obj' : details_obj,
        'random_post' : random_post,
    }

    return render(request,'blog/details.html', context)

@login_required
def addPost(request):

    if request.method == 'POST' and 'btn-search' in request.POST:
        q = request.POST.get('search').strip()
        if q:
            request.session['q'] = q
            return redirect('blog_search')
    
    if request.method == 'POST'  and 'blog_submit' in request.POST:
        form = blogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.blog_user = request.user
            post_item.slug = request.user
            # info.user_id = request.user.id
            post_item.save()
            return redirect('blog_home')
           
    else:
        form = blogPostForm()
    return render(request,'blog/add_post.html', {'form':form})


@login_required
def blog_edit(request, id):

    if request.method == 'POST' and 'btn-search' in request.POST:
        q = request.POST.get('search').strip()
        if q:
            request.session['q'] = q
            return redirect('blog_search')
    
    post = blogPost.objects.get(id=id)

    if request.user == post.blog_user:
        item = get_object_or_404(blogPost, id=id)
        form = blogPostForm(request.POST or None,request.FILES or None, instance=item)

        if form.is_valid():
            obj= form.save(commit= False)
            obj.save()

            return redirect('blog_details', id)
    else:
        return redirect('blog_details', id)

    
    return render(request, 'blog/add_post.html', {'form' : form})


@login_required
def blog_delete(request, id):

    if request.method == 'POST' and 'btn-search' in request.POST:
        q = request.POST.get('search').strip()
        if q:
            request.session['q'] = q
            return redirect('blog_search')
    
    post = blogPost.objects.get(id=id)

    if request.user == post.blog_user:
        item = get_object_or_404(blogPost, id=id)
        item.delete()

        return redirect('user_post', request.user)
    else:
        return redirect('user_post', request.user)

    return render(request, 'blog/delete.html', {'post' : post})


def user_post(request, slug):

    if request.method == 'POST' and 'btn-search' in request.POST:
        q = request.POST.get('search').strip()
        if q:
            request.session['q'] = q
            return redirect('blog_search')

    # di_count = division_post_count()
    
    post1 = blogPost.objects.filter(slug=slug).order_by('id')
    post = blogPost.objects.filter(slug=slug).order_by('-id')
    paginator = Paginator(post, 5)  # Show 10 obj per page
    random_post = blogPost.objects.order_by('?')

    page = request.GET.get('page')
    post = paginator.get_page(page)

    context = {
        'di_count' : division_post_count(),
        'post':post, 
        'post1':post1,
        'random_post' : random_post,
    }

    # post = get_object_or_404(blogPost, blog_user=request.user)
    # print(post)

    # post = blogPost.objects.get(blog_user=request.user)

    return render(request, 'blog/user_post.html', context)



def division_post(request, slug):

    if request.method == 'POST' and 'btn-search' in request.POST:
        q = request.POST.get('search').strip()
        if q:
            request.session['q'] = q
            return redirect('blog_search')

    # di_count = division_post_count()

    post1 = blogPost.objects.filter(division=slug).order_by('id')
    post = blogPost.objects.filter(division=slug).order_by('-id')
    paginator = Paginator(post, 5)  # Show 10 obj per page
    random_post = blogPost.objects.order_by('?')

    page = request.GET.get('page')
    post = paginator.get_page(page)

    context = {
        'di_count' : division_post_count(),
        'post':post, 
        'post1':post1,
        'random_post' : random_post,
    }

    # post = get_object_or_404(blogPost, blog_user=request.user)
    # print(post)

    # post = blogPost.objects.get(blog_user=request.user)

    return render(request, 'blog/division_post.html', context)


def blog_search(request):

    q = request.session.get('q')
    post_query = blogPost.objects.all().filter(
        Q(title__icontains=q)|
		Q(description__icontains=q)|
		Q(division__icontains=q))
    paginator = Paginator(post_query, 10)  # Show 10 obj per page

    page = request.GET.get('page')
    post = paginator.get_page(page)

    context = {
        
        'di_count' : division_post_count(),
        'post' : post,
        'query':q,
    }

    return render(request, 'blog/blog_search.html', context)