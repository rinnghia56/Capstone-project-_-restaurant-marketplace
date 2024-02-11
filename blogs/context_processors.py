from .models import CategoryBlog


def get_category_post(request):
    list_category_blog = CategoryBlog.objects.all()
    return dict(list_category_blog=list_category_blog)