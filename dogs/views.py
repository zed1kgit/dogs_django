from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

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
        'object_list': Dog.objects.filter(category_id=pk),
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


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        return reverse_lazy('dogs:detail_dog', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        if self.request.user != self.object.owner and not self.request.user.is_staff:
            raise Http404
        return self.object


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        if self.request.user != self.object.owner and not self.request.user.is_staff:
            raise Http404
        return self.object
