from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from dogs.models import Category, Dog, Parent
from dogs.forms import DogForm, ParentForm, DogAdminForm
from dogs.services import send_congratulation_mail
from users.models import UserRoles


def index(request):
    """Рендер главной страницы"""
    context = {
        'category_object_list': Category.objects.all()[:3],
        'title': 'Главная'
    }
    return render(request, 'dogs/index.html', context)


class CategoryListView(ListView, LoginRequiredMixin):
    model = Category
    extra_context = {
        'title': 'Все наши породы'
    }
    template_name = 'dogs/categories.html'


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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivateListView(ListView, LoginRequiredMixin):
    model = Dog
    extra_context = {
        'title': 'Неактивные собаки'
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        elif self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def form_valid(self, form):
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        if self.request.user != self.object.owner:
            self.object.view_count += 1
            self.object.save()
            if self.object.view_count == 100 and self.object.owner:
                send_congratulation_mail(self.object.owner, self.object, 100)
            return self.object
        return self.object


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        return reverse_lazy('dogs:detail_dog', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        if self.request.user != self.object.owner and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ParentFormset = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)
        else:
            formset = ParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        if self.request.user.role == UserRoles.ADMIN:
            form_class = DogAdminForm
        else:
            form_class = DogForm
        return form_class


class DogDeleteView(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')
    permission_required = ('dogs.delete_dog',)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        if self.request.user != self.object.owner and not self.request.user.is_staff:
            raise Http404
        return self.object


def dog_toggle_activity(request, pk):
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:list_dogs'))
