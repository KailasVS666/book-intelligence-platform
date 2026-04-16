from django.urls import path
from .views import get_books, get_book, recommend_books, ask_question, upload_book

urlpatterns = [
    path('books/', get_books),
    path('books/upload/', upload_book),
    path('books/<int:pk>/', get_book),
    path('books/<int:pk>/recommend/', recommend_books),
    path('ask/', ask_question),
]