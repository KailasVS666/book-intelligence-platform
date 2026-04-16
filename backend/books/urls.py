from django.urls import path
from .views import get_books, get_book

urlpatterns = [
    path('books/', get_books),
    path('books/<int:pk>/', get_book),
]