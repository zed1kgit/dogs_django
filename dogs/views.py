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


def dog_detail_view(request, pk):
    """Рендер страницы отображающая выбранную собаку"""
    context = {
        'object': Dog.objects.get(pk=pk),
        'title': 'Вы выбрали данную собаку'
    }
    return render(request, 'dogs/detail.html', context)


def dog_update_view(request, pk):
    """Рендер страницы редактирования выбранной собаки"""
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save()
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:detail_dog', args={pk: pk}))
    context = {
        'object': dog_object,
        'form': DogForm(instance=dog_object)
    }
    return render(request, 'dogs/create_update.html', context)


def dog_delete_view(request, pk):
    """Рендер страницы и удаление выбранной собаки"""
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        dog_object.delete()
        return HttpResponseRedirect(reverse('dogs:list_dogs'))
    return render(request, 'dogs/delete.html', {
        'object': dog_object,
    }, )
