from django.contrib import admin

from dogs.models import Dog, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk']
    ordering = ['pk']


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    ordering = ['name']
