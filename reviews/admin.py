from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'dog', 'author', 'timestamp', 'sign_of_review']
    ordering = ('timestamp',)
    list_filter = ('dog', 'author',)
