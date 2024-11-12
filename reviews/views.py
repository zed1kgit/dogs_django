from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from reviews.forms import ReviewForm
from reviews.models import Review


class DogReviewListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Отзывы о собаке',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(dog_id=self.kwargs['pk'])
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class InactiveDogReviewListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Неактивные отзывы о собаке',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(dog_pk=self.kwargs['pk'])
        queryset = queryset.filter(sign_of_review=False)
        return queryset


class DogReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm


class DogReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm


class DogReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review


class DogReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
