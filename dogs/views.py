from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from dogs.models import Category, Dog
from dogs.forms import DogForm

def index(request):
    """Рендер главной страницы"""
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Главная'
    }
    return render(request, 'dogs/index.html', context)


def categories(request):
    """Рендер страницы пород"""
    context = {
        'object_list': Category.objects.all(),
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


def dogs_list_view(request):
    """Рендер страницы со всеми собаками"""
    context = {
        'object_list': Dog.objects.all(),
        'title': 'Все собаки',
    }
    return render(request, 'dogs/dogs.html', context)


def dog_create_view(request):
    """Рендер страницы с созданием новой собаки"""
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dogs:list_dogs'))
    return render(request, 'dogs/create_update.html', {'form': DogForm()})


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
    return render(request, 'dogs/create_update.html', {
        'object': dog_object,
        'form': DogForm(instance=dog_object)
    }, )


def dog_delete_view(request, pk):
    """Рендер страницы и удаление выбранной собаки"""
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        dog_object.delete()
        return HttpResponseRedirect(reverse('dogs:list_dogs'))
    return render(request, 'dogs/delete.html', {
        'object': dog_object,
    }, )