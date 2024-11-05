from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from dogs.models import Category, Dog
from dogs.forms import DogForm


def index(request):
    """Рендер главной страницы"""
    context = {
        'category_object_list': Category.objects.all()[:3],
        'title': 'Главная'
    }
    return render(request, 'dogs/index.html', context)


def categories(request):
    """Рендер страницы пород"""
    context = {
        'category_object_list': Category.objects.all(),
        'title': 'Породы'
    }
    return render(request, 'dogs/categories.html', context)


def category_dogs(request, pk):
    """Рендер страницы с собаками определенной породы"""
    category_item = Category.objects.get(pk=pk)
    context = {
        'dog_object_list': Dog.objects.filter(category_id=pk),
        'title': f'Собаки породы - {category_item.name}',
        'category_pk': category_item.pk,
    }
    return render(request, 'dogs/dogs.html', context)


class DogListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Все наши собаки'
    }
    template_name = 'dogs/dogs.html'


class DogCreateView(CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'


class DogUpdateView(UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        return reverse_lazy('dogs:detail_dog', kwargs={'pk': self.object.pk})


class DogDeleteView(DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    reverse_lazy('dogs:list_dogs')
