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
    model = Review
    extra_context = {
        'title': 'Отзывы о всех собаках',
        'all': True,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class AllInactiveDogReviewListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Все неактивные отзывы о собаках',
        'all': True,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(sign_of_review=False)
        elif self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(sign_of_review=False, author=self.request.user)
        return queryset


class DogReviewListView(LoginRequiredMixin, ListView):
    model = Review

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(dog_id=self.kwargs['pk'])
        queryset = queryset.filter(sign_of_review=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Отзывы о собаке: {get_object_or_404(Dog, pk=self.kwargs['pk'])}'
        context['pk'] = self.kwargs['pk']
        return context


class InactiveDogReviewListView(LoginRequiredMixin, ListView):
    model = Review

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(sign_of_review=False, dog_id=self.kwargs['pk'])
        elif self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(sign_of_review=False, dog_id=self.kwargs['pk'], author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Неактивные отзывы о собаке: {get_object_or_404(Dog, pk=self.kwargs['pk'])}'
        context['pk'] = self.kwargs['pk']
        return context


class DogReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm

    def get_success_url(self):
        return reverse('reviews:review_detail', args=[self.kwargs['slug']])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author == self.request.user or self.request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            return self.object
        raise PermissionDenied


class DogReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
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
        return reverse('reviews:review_detail', args=[self.object.slug])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class DogReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Review
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        return reverse('reviews:reviews_list', args=[self.object.dog.pk])


class DogReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review


def review_toggle_activity(request, slug):
    review = get_object_or_404(Review, slug=slug)
    if review.sign_of_review:
        review.sign_of_review = False
        review.save()
        return HttpResponseRedirect(reverse('reviews:inactive_reviews_list', args=[review.dog.pk]))
    else:
        review.sign_of_review = True
        review.save()
        return HttpResponseRedirect(reverse('reviews:reviews_list', args=[review.dog.pk]))
