from django.urls import path
from .views import (
    BookListCreateView, 
    BookDetailView, 
    BookRecommendationView, 
    BookUploadView, 
    AskQuestionView
)

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('<int:pk>/recommendations/', BookRecommendationView.as_view(), name='book-recommendations'),
    path('upload/', BookUploadView.as_view(), name='book-upload'),
    path('ask/', AskQuestionView.as_view(), name='book-ask'),
]