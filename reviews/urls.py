from django.urls import path

from reviews.views import DogReviewListView, InactiveDogReviewListView, DogReviewCreateView, DogReviewUpdateView, \
    DogReviewDeleteView, DogReviewDetailView, AllDogReviewListView, AllInactiveDogReviewListView
from reviews.apps import ReviewsConfig

app_name = ReviewsConfig.name

urlpatterns = [
    path('', AllDogReviewListView.as_view(), name='all_reviews'),
    path('inactive/', AllInactiveDogReviewListView.as_view(), name='all_inactive_reviews'),
    path('<int:pk>/', DogReviewListView.as_view(), name='reviews_list'),
    path('<int:pk>/inactive/', InactiveDogReviewListView.as_view(), name='inactive_reviews_list'),
    path('<int:pk>/create/', DogReviewCreateView.as_view(), name='review_create'),
    path('<int:pk>/update/', DogReviewUpdateView.as_view(), name='review_update'),
    path('<int:pk>/delete/', DogReviewDeleteView.as_view(), name='review_delete'),
    path('<int:pk>/detail/', DogReviewDetailView.as_view(), name='review_detail'),
]
