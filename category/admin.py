from django.contrib import admin
from .models import Category

# Register your models here.
# 1-> register category model
# for prepoupulated slug we have to create class
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)

