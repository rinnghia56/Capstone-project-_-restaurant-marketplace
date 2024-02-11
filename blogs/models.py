from django.db import models
from accounts.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class CategoryBlog(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name) + '-' + str(self.id)
        return super(CategoryBlog, self).save(*args, **kwargs)
    
class Post(models.Model):
    category = models.ForeignKey(CategoryBlog, on_delete=models.CASCADE,  related_name='postitems')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField(blank=True, max_length=50000)
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='postimages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.post_title) + '-' + str(self.id)
        return super(Post, self).save(*args, **kwargs)