from django.urls import path
from .views import get_books, get_book, recommend_books

urlpatterns = [
    path('books/', get_books),
    path('books/<int:pk>/', get_book),
    path('books/<int:pk>/recommend/', recommend_books),
]