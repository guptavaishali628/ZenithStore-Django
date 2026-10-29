from django.db import models

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=50)
    slug=models.CharField(max_length=100, unique=True)
    Description=models.TextField(max_length=255)
    cat_image=models.ImageField(upload_to='photos/categories', blank=True)

    # verbose name to change categorys to categories
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    # string representation of model
    def __str__(self):
        return self.category_name