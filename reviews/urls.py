from django.urls import path

from reviews.views import DogReviewListView, InactiveDogReviewListView, DogReviewCreateView, DogReviewUpdateView, \
    DogReviewDeleteView, DogReviewDetailView
from reviews.apps import ReviewsConfig

app_name = ReviewsConfig.name

urlpatterns = [
    path('<int:pk>/reviews/', DogReviewListView.as_view(), name='reviews_list'),
    path('<int:pk>/reviews/inactive/', InactiveDogReviewListView.as_view(), name='inactive_review_list'),
    path('<int:pk>/reviews/create/', DogReviewCreateView.as_view(), name='review_create'),
    path('<int:pk>/reviews/update/', DogReviewUpdateView.as_view(), name='review_update'),
    path('<int:pk>/reviews/delete/', DogReviewDeleteView.as_view(), name='review_delete'),
    path('<int:pk>/reviews/detail/', DogReviewDetailView.as_view(), name='review_detail'),
]
