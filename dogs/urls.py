from  django.urls import path

import dogs
from dogs.views import index, categories, category_dogs, dogs_list_view, dog_create_view
from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('categories/', categories, name='categories'),
    path('categories/<int:pk>/dogs/', category_dogs, name='category_dogs'),
    path('dogs/', dogs_list_view, name='list_dogs'),
    path('dogs/create', dog_create_view, name='create_dogs'),
]
