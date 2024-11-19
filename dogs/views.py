from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q

from dogs.models import Category, Dog, Parent
from dogs.forms import DogForm, ParentForm, DogAdminForm
from users.models import UserRoles


def index(request):
    """
    Отображение главной страницы сайта.

    Параметры:
        request (HttpRequest): Запрос от клиента.

    Контекст:
        category_object_list (QuerySet): Список первых трех записей из таблицы категорий.
        title (str): Заголовок страницы.

    Возвращает:
        HttpResponse: Ответ с рендером главной страницы.
    """
    context = {
        'category_object_list': Category.objects.all()[:3],
        'title': 'Главная'
    }
    return render(request, 'dogs/index.html', context)


class CategoryListView(LoginRequiredMixin, ListView):
    """
    Представление списка всех категорий.

    Атрибуты:
        model (Model): Модель категории.
        extra_context (dict): Дополнительный контекст для шаблона.
        template_name (str): Имя файла шаблона.
    """
    model = Category
    extra_context = {
        'title': 'Все наши породы'
    }
    template_name = 'dogs/categories.html'


def category_dogs(request, pk):
    """
    Отображение страницы с собаками определенной породы.

    Параметры:
        request (HttpRequest): Запрос от клиента.
        pk (int): Первичный ключ категории.

    Контекст:
        object_list (QuerySet): Список собак выбранной категории.
        title (str): Заголовок страницы.
        category_pk (int): Идентификатор категории.

    Возвращает:
        HttpResponse: Ответ с рендером страницы с собаками определенной породы.
    """
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),
        'title': f'Собаки породы - {category_item.name}',
        'category_pk': category_item.pk,
    }
    return render(request, 'dogs/dogs.html', context)


class DogListView(ListView):
    """
    Представление списка активных собак.

    Атрибуты:
        model (Model): Модель собаки.
        paginate_by (int): Количество объектов на странице.
        extra_context (dict): Дополнительный контекст для шаблона.
        template_name (str): Имя файла шаблона.

    Методы:
        get_queryset(): Переопределенный метод получения QuerySet, который фильтрует активные собаки.
    """
    model = Dog
    paginate_by = 6
    extra_context = {
        'title': 'Все наши собаки'
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        """
        Получение QuerySet с активными собаками.

        Возвращает:
            QuerySet: Фильтрованный список активных собак.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivateListView(LoginRequiredMixin, ListView):
    """
    Представление списка неактивных собак.

    Атрибуты:
        model (Model): Модель собаки.
        extra_context (dict): Дополнительный контекст для шаблона.
        template_name (str): Имя файла шаблона.

    Методы:
        get_queryset(): Переопределенный метод получения QuerySet, который фильтрует неактивные собаки в зависимости от роли пользователя.
    """
    model = Dog
    extra_context = {
        'title': 'Неактивные собаки'
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        """
        Получение QuerySet с неактивными собаками.

        Возвращает:
            QuerySet: Фильтрованный список неактивных собак в зависимости от роли пользователя.
        """
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        elif self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogSearchListView(LoginRequiredMixin, ListView):
    """
    Представление списка результатов поиска собак.

    Атрибуты:
        model (Model): Модель собаки.
        template_name (str): Имя файла шаблона.

    Методы:
        get_queryset(): Переопределенный метод получения QuerySet, который фильтрует результаты поиска.
        get_context_data(**kwargs): Переопределенный метод добавления дополнительного контекста для шаблона.
    """
    model = Dog
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        """
        Получение QuerySet с результатами поиска собак.

        Параметры:
            q (str): Строка запроса.

        Возвращает:
            QuerySet: Фильтрованный список собак, соответствующих запросу.
        """
        query = self.request.GET.get('q')
        object_list = Dog.objects.filter(
            Q(name__icontains=query), is_active=True,
        )
        return object_list

    def get_context_data(self, **kwargs):
        """
        Добавление дополнительного контекста для шаблона.

        Параметры:
            **kwargs: Аргументы ключевого слова.

        Возвращает:
            dict: Обновленный контекст для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Поиск собаки: {self.request.GET.get("q")}'
        return context


class CategorySearchListView(LoginRequiredMixin, ListView):
    """
    Представление списка результатов поиска пород собак.

    Атрибуты:
        model (Model): Модель категории.
        template_name (str): Имя файла шаблона.

    Методы:
        get_queryset(): Переопределенный метод получения QuerySet, который фильтрует результаты поиска.
        get_context_data(**kwargs): Переопределенный метод добавления дополнительного контекста для шаблона.
    """
    model = Category
    template_name = 'dogs/categories.html'

    def get_queryset(self):
        """
        Получение QuerySet с результатами поиска пород собак.

        Параметры:
            q (str): Строка запроса.

        Возвращает:
            QuerySet: Фильтрованный список категорий, соответствующих запросу.
        """
        query = self.request.GET.get('q')
        object_list = Category.objects.filter(
            Q(name__icontains=query),
        )
        return object_list

    def get_context_data(self, **kwargs):
        """
        Добавление дополнительного контекста для шаблона.

        Параметры:
            **kwargs: Аргументы ключевого слова.

        Возвращает:
            dict: Обновленный контекст для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Поиск породы: {self.request.GET.get("q")}'
        return context


class DogCreateView(LoginRequiredMixin, CreateView):
    """
    Представление создания новой собаки.

    Атрибуты:
        model (Model): Модель собаки.
        form_class (Form): Форма для создания собаки.
        template_name (str): Имя файла шаблона.
        success_url (str): URL для перенаправления после успешного сохранения.

    Методы:
        form_valid(form): Переопределенный метод обработки формы при успешной валидации.
    """
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def form_valid(self, form):
        """
        Обработка формы при успешной валидации.

        Параметры:
            form (DogForm): Форма для создания собаки.

        Исключения:
            PermissionDenied: Если пользователь не является пользователем.

        Возвращает:
            HttpResponseRedirect: Перенаправление на страницу успеха.
        """
        if self.request.user.role != UserRoles.USER:
            raise PermissionDenied()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    """
    Представление детальной информации о собаке.

    Атрибуты:
        model (Model): Модель собаки.
        template_name (str): Имя файла шаблона.

    Методы:
        get_object(queryset=None): Переопределенный метод получения объекта.
    """
    model = Dog
    template_name = 'dogs/detail.html'

    def get_object(self, queryset=None):
        """
        Получение объекта собаки.

        Параметры:
            queryset (QuerySet): Набор запросов.

        Возвращает:
            Dog: Объект собаки.

        Исключения:
            Http404: Если объект не найден.
        """
        self.object = super().get_object(queryset=queryset)
        if self.request.user != self.object.owner:
            self.object.view_count += 1
            self.object.save()
        return self.object


class DogUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление обновления информации о собаке.

    Атрибуты:
        model (Model): Модель собаки.
        template_name (str): Имя файла шаблона.

    Методы:
        get_success_url(): Получение URL для перенаправления после успешного обновления.
        get_object(queryset=None): Переопределенный метод получения объекта.
        get_context_data(**kwargs): Переопределенный метод добавления дополнительного контекста для шаблона.
        form_valid(form): Переопределенный метод обработки формы при успешной валидации.
        get_form_class(): Получение класса формы в зависимости от роли пользователя.
    """
    model = Dog
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешного обновления.

        Возвращает:
            str: URL для перенаправления.
        """
        return reverse_lazy('dogs:detail_dog', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        """
        Получение объекта собаки.

        Параметры:
            queryset (QuerySet): Набор запросов.

        Возвращает:
            Dog: Объект собаки.

        Исключения:
            PermissionDenied: Если пользователь не является владельцем или администратором.
        """
        self.object = super().get_object(queryset=queryset)
        if self.request.user != self.object.owner and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied()
        return self.object

    def get_context_data(self, **kwargs):
        """
        Добавление дополнительного контекста для шаблона.

        Параметры:
            **kwargs: Аргументы ключевого слова.

        Возвращает:
            dict: Обновленный контекст для шаблона.
        """
        context_data = super().get_context_data(**kwargs)
        ParentFormset = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)
        else:
            formset = ParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        """
        Обработка формы при успешной валидации.

        Параметры:
            form (DogForm): Форма для обновления собаки.

        Возвращает:
            HttpResponseRedirect: Перенаправление на страницу успеха.
        """
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        """
        Получение класса формы в зависимости от роли пользователя.

        Возвращает:
            Form: Класс формы для обновления собаки.
        """
        if self.request.user.role == UserRoles.ADMIN:
            form_class = DogAdminForm
        else:
            form_class = DogForm
        return form_class


class DogDeleteView(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """
    Представление удаления собаки.

    Атрибуты:
        model (Model): Модель собаки.
        template_name (str): Имя файла шаблона.
        success_url (str): URL для перенаправления после успешного удаления.
        permission_required (tuple): Требуемые разрешения.

    Методы:
        get_object(queryset=None): Переопределенный метод получения объекта.
    """
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')
    permission_required = ('dogs.delete_dog',)

    def get_object(self, queryset=None):
        """
        Получение объекта собаки.

        Параметры:
            queryset (QuerySet): Набор запросов.

        Возвращает:
            Dog: Объект собаки.

        Исключения:
            Http404: Если объект не найден.
        """
        self.object = super().get_object(queryset=queryset)
        if self.request.user != self.object.owner and not self.request.user.is_staff:
            raise Http404
        return self.object


def dog_toggle_activity(request, pk):
    """
    Переключение активности собаки.

    Параметры:
        request (HttpRequest): Запрос от клиента.
        pk (int): Первичный ключ собаки.

    Возвращает:
        HttpResponseRedirect: Перенаправление на страницу списка собак.

    Исключения:
        Http404: Если собака не найдена.
    """
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:list_dogs'))
