from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import blogPostForm
from django.contrib.auth.decorators import login_required
from blog.models import blogPost
from django.core.paginator import Paginator


# Create your views here.
def search(request):
    return render(request,'blog/home.html')

# def home(request):

#     allpost = blogPost.objects.all().order_by('-id')
#     paginator = Paginator(allpost, 2)  # Show 10 obj per page

#     page = request.GET.get('page')
#     allpost = paginator.get_page(page)

#     context = {
#         # 'paginator_pages': paginator_pages,
#         'allpost' : allpost,
#     }
    

#     return render(request,'blog/home.html', context)

# def details(request, id):

#     details_obj = blogPost.objects.get(id = id)

#     return render(request,'blog/details.html', {'details_obj' : details_obj})

# @login_required
# def addPost(request):
    
#     if request.method == 'POST'  and 'blog_submit' in request.POST:
#         form = blogPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post_item = form.save(commit=False)
#             post_item.blog_user = request.user
#             post_item.slug = request.user
#             # info.user_id = request.user.id
#             post_item.save()
#             return redirect('blog_home')
           
#     else:
#         form = blogPostForm()
#     return render(request,'blog/add_post.html', {'form':form})


# @login_required
# def blog_edit(request, id):
    
#     post = blogPost.objects.get(id=id)

#     if request.user == post.blog_user:
#         item = get_object_or_404(blogPost, id=id)
#         form = blogPostForm(request.POST or None,request.FILES or None, instance=item)

#         if form.is_valid():
#             obj= form.save(commit= False)
#             obj.save()

#             return redirect('blog_home')
#     else:
#         pass

    
#     return render(request, 'blog/add_post.html', {'form' : form})


# @login_required
# def blog_delete(request, id):
    
#     post = blogPost.objects.get(id=id)

#     if request.user == post.blog_user:
#         item = get_object_or_404(blogPost, id=id)
#         item.delete()

#         return redirect('blog_home')
#     else:
#         pass

#     return render(request, 'blog/delete.html', {'post' : post})


# def user_post(request, slug):
    
#     post = blogPost.objects.filter(slug=slug).order_by('-id')
#     paginator = Paginator(post, 2)  # Show 10 obj per page

#     page = request.GET.get('page')
#     post = paginator.get_page(page)

#     # post = get_object_or_404(blogPost, blog_user=request.user)
#     # print(post)

#     # post = blogPost.objects.get(blog_user=request.user)

#     return render(request, 'blog/user_post.html', {'post':post})
