from django.db import models
from vendor.models import Vendor
from accounts.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator

# Create your models here.
class CategoryDefault(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    image = models.ImageField(upload_to='categoty_default', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name) + '-' + str(self.id) +'default'
        return super(CategoryDefault, self).save(*args, **kwargs)



# Create your models here.
class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name) + '-' + str(self.id)
        return super(Category, self).save(*args, **kwargs)



class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_default = models.ForeignKey(CategoryDefault, on_delete=models.CASCADE, default=None, related_name="fooditems_default")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  related_name='fooditems')
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=5000)
    ingredients = models.TextField(blank=True, max_length=5000)
    notice = models.TextField(blank=True, max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5)],null = True,blank = True)
    rating_count = models.IntegerField(default=0, null = True,blank = True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_title
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.food_title) + '-' + str(self.id)
        return super(FoodItem, self).save(*args, **kwargs)


class FoodImage(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='food_images')
    image = models.ImageField(upload_to='foodimagedetails')

    def __str__(self):
        return self.image.name
    
class FoodFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email 
