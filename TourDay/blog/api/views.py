from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from blog.serializers import blogPostSerializer, blogCreateSerializer
from blog.models import blogPost

@api_view(['GET', ])
def api_home(request):

    paginator = PageNumberPagination()
    paginator.page_size = 1

    try:
        allpost = blogPost.objects.all().order_by('-id')
        post = paginator.paginate_queryset(allpost, request)
        serializer = blogPostSerializer(post, many=True)
        return paginator.get_paginated_response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # bad request

@api_view(['GET',])
def api_details(request, id):
    try:
        details_obj = blogPost.objects.get(id=id)
        serializer = blogPostSerializer(details_obj, many=False)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # bad request


@api_view(['GET',])
def api_user_post(request, slug):

    paginator = PageNumberPagination()
    paginator.page_size = 1

    try:

        user_post = blogPost.objects.filter(slug=slug).order_by('-id')
       
        post = paginator.paginate_queryset(user_post, request)
        serializer = blogPostSerializer(post, many=True)
        return paginator.get_paginated_response(serializer.data)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # bad request

@api_view(['GET',])
def api_division_post(request, slug):

    paginator = PageNumberPagination()
    paginator.page_size = 1

    try:
        division_post = blogPost.objects.filter(division=slug).order_by('-id')
        post = paginator.paginate_queryset(division_post, request)
        serializer = blogPostSerializer(post, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_addpost(request):
    
    blog_post = blogPost()

    try:
        if request.method == 'POST':
            blog_post.blog_user = request.user
            blog_post.slug = request.user

            serializer = blogCreateSerializer(blog_post, data=request.data)


            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_blogEdit(request, id):

    try:
        post = blogPost.objects.get(id=id)

    except blogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        if request.user == post.blog_user:
            serializer = blogCreateSerializer(post, data=request.data)
            data={}
            if serializer.is_valid():
                serializer.save()

                data['success'] = "Update Successfully."
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_blogDelete(request, id):

    try:
        post = blogPost.objects.get(id=id)

    except blogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if request.user == post.blog_user:
            operation = post.delete()

            data = {}

            if operation:
                data['success'] = 'Delete Successfully.'
            else:
                data['failure'] = 'Delete Failure'
            return Response(data=data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    