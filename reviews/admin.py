from django.contrib import admin

from reviews.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'dog', 'pk']
    ordering = ('timestamp',)
    search_fields = ('dog', 'title',)
