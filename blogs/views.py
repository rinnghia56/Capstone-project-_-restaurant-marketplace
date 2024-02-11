from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, CategoryBlog

# view list blog
def list_blog(request):
    list_post = Post.objects.filter(is_approved=True)
    context = {
        "list_post":list_post[:4]
    }
    return render(request,'blogs/list_blog.html',context)

# view post by category
def list_blog_by_category(request,category_slug):
    category = get_object_or_404(CategoryBlog, slug=category_slug)
    posts = Post.objects.filter(is_approved=True, category = category)
    context = {
        "posts":posts
    }
    return render(request,'blogs/posts_by_category.html',context)

# view post detail
def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    context = {
        "post":post
    }
    return render(request,'blogs/post_detail.html',context)