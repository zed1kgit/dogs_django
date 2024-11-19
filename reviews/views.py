from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from dogs.models import Dog
from reviews.forms import ReviewForm
from reviews.models import Review
from reviews.utils import slug_generator
from users.models import UserRoles


class AllDogReviewListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка всех активированных отзывов о собаках.

    Атрибуты:
        model (Review): Модель отзывов.
        paginate_by (int): Количество отзывов на одной странице.
        extra_context (dict): Дополнительный контекст для передачи в шаблон.

    Метод:
        get_queryset(self):
 Получение набора активированных отзывов.
    """

    model = Review
    paginate_by = 3
    extra_context = {
        'title': 'Отзывы о всех собаках',
        'all': True,
    }

    def get_queryset(self):
        """
        Получение набора активированных отзывов.

        Возвращает:
            QuerySet: Набор активированных отзывов.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class AllInactiveDogReviewListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка всех неактивных отзывов о собаках.

    Атрибуты:
        model (Review): Модель отзывов.
        paginate_by (int): Количество отзывов на одной странице.
        extra_context (dict): Дополнительный контекст для передачи в шаблон.

    Метод:
        get_queryset(self): Получение набора неактивированных отзывов в зависимости от роли пользователя.
    """

    model = Review
    paginate_by = 3
    extra_context = {
        'title': 'Все неактивные отзывы о собаках',
        'all': True,
    }

    def get_queryset(self):
        """
        Получение набора неактивированных отзывов в зависимости от роли пользователя.

        Возвращает:
            QuerySet: Набор неактивированных отзывов.
        """
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(sign_of_review=False)
        elif self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(sign_of_review=False, author=self.request.user)
        return queryset


class DogReviewListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка активированных отзывов о конкретной собаке.

    Атрибуты:
        model (Review): Модель отзывов.
        paginate_by (int): Количество отзывов на одной странице.

    Методы:
        get_queryset(self): Получение набора активированных отзывов о конкретной собаке.
        get_context_data(self, **kwargs): Формирование дополнительного контекста для передачи в шаблон.
    """

    model = Review
    paginate_by = 3

    def get_queryset(self):
        """
        Получение набора активированных отзывов о конкретной собаке.

        Возвращает:
            QuerySet: Набор активированных отзывов о конкретной собаке.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(dog_id=self.kwargs['pk'])
        queryset = queryset.filter(sign_of_review=True)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Формирование дополнительного контекста для передачи в шаблон.

        Аргументы:
            **kwargs: Именованные аргументы.

        Возвращает:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Отзывы о собаке: {get_object_or_404(Dog, pk=self.kwargs['pk'])}'
        context['pk'] = self.kwargs['pk']
        return context


class InactiveDogReviewListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка неактивированных отзывов о конкретной собаке.

    Атрибуты:
        model (Review): Модель отзывов.
        paginate_by (int): Количество отзывов на одной странице.

    Методы:
        get_queryset(self): Получение набора неактивированных отзывов о конкретной собаке в зависимости от роли пользователя.
        get_context_data(self, **kwargs): Формирование дополнительного контекста для передачи в шаблон.
    """

    model = Review
    paginate_by = 3

    def get_queryset(self):
        """
        Получение набора неактивированных отзывов о конкретной собаке в зависимости от роли пользователя.

        Возвращает:
            QuerySet: Набор неактивированных отзывов о конкретной собаке.
        """
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(sign_of_review=False, dog_id=self.kwargs['pk'])
        elif self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(sign_of_review=False, dog_id=self.kwargs['pk'], author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Формирование дополнительного контекста для передачи в шаблон.

        Аргументы:
            **kwargs: Именованные аргументы.

        Возвращает:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Неактивные отзывы о собаке: {get_object_or_404(Dog, pk=self.kwargs['pk'])}'
        context['pk'] = self.kwargs['pk']
        return context


class DogReviewUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления отзыва.

    Атрибуты:
        model (Review): Модель отзывов.
        form_class (ReviewForm): Форма для редактирования отзыва.

    Методы:
        get_success_url(self): Получение URL для перенаправления после успешного сохранения изменений.
        get_object(self, queryset=None): Получение объекта отзыва для редактирования.
    """

    model = Review
    form_class = ReviewForm

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешного сохранения изменений.

        Возвращает:
            str: URL для перенаправления на страницу с подробностями отзыва.
        """
        return reverse('reviews:review_detail', args=[self.kwargs['slug']])

    def get_object(self, queryset=None):
        """
        Получение объекта отзыва для редактирования.

        Аргументы:
            queryset (QuerySet): Набор объектов модели. По умолчанию None.

        Возвращает:
            Review: Объект отзыва.

        Исключения:
            PermissionDenied: Если текущий пользователь не является автором отзыва и не имеет прав администратора/модератора.
        """
        self.object = super().get_object(queryset)
        if self.object.author == self.request.user or self.request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return self.object
        raise PermissionDenied


class DogReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания отзыва о собаке.

    Атрибуты:
        model (Review): Модель отзывов.
        form_class (ReviewForm): Форма для создания отзыва.


    Методы:
        form_valid(self, form): Обработка формы после ее заполнения.
        get_success_url(self): Получение URL для перенаправления после успешного создания отзыва.
        get_context_data(self, **kwargs): Формирование дополнительного контекста для передачи в шаблон.
    """

    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        """
        Обработка формы после ее заполнения.

        Аргументы:
            form (ReviewForm): Заполненная форма для создания отзыва.

        Возвращает:
            HttpResponse: Ответ на запрос, который зависит от роли пользователя.
        """
        if self.request.user.role not in [UserRoles.USER, UserRoles.ADMIN]:
            return HttpResponseForbidden()
        if not form.instance.dog_id:
            form.instance.dog_id = self.kwargs['pk']
        self.object = form.save()
        if self.object.slug == 'temp_slug':
            self.object.slug = slug_generator()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешного создания отзыва.

        Возвращает:
            str: URL для перенаправления на страницу с подробностями созданного отзыва.
        """
        return reverse('reviews:review_detail', args=[self.object.slug])

    def get_context_data(self, **kwargs):
        """
        Формирование дополнительного контекста для передачи в шаблон.

        Аргументы:
            **kwargs: Именованные аргументы.

        Возвращает:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DogReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления отзыва.

    Атрибуты:
        model (Review): Модель отзывов.
        permission_required (str): Право, необходимое для удаления отзыва.

    Методы:
        get_success_url(self): Получение URL для перенаправления после успешного удаления отзыва.
    """

    model = Review
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        """
        Получение URL для перенаправления после успешного удаления отзыва.

        Возвращает:
            str: URL для перенаправления на список отзывов о данной собаке.
        """
        return reverse('reviews:reviews_list', args=[self.object.dog.pk])


class DogReviewDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей конкретного отзыва.

    Атрибуты:
        model (Review): Модель отзывов.
    """

    model = Review


def review_toggle_activity(request, slug):
    """
    Переключение статуса активности отзыва.

    Аргументы:
        request (HttpRequest): Запрос от клиента.
        slug (str): Уникальный слаг отзыва.

    Возвращает:
        HttpResponseRedirect: Перенаправление на соответствующий список отзывов.
    """
    review = get_object_or_404(Review, slug=slug)
    if review.sign_of_review:
        review.sign_of_review = False
        review.save()
        return HttpResponseRedirect(reverse('reviews:inactive_reviews_list', args=[review.dog.pk]))
    else:
        review.sign_of_review = True
        review.save()
        return HttpResponseRedirect(reverse('reviews:reviews_list', args=[review.dog.pk]))
