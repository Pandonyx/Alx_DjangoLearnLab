from django.urls import path
from . import views

urlpatterns = [
    # Book URLs
    # Book ListView - GET /books/
    path('books/', views.BookListView.as_view(), name='book-list'),
    
    # Book CreateView - POST /books/create/
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # Book DetailView - GET /books/<int:pk>/
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Book UpdateView - PUT/PATCH /books/<int:pk>/update/
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    
    # Book DeleteView - DELETE /books/<int:pk>/delete/
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author URLs
    # Author ListView - GET /authors/
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    
    # Author DetailView - GET /authors/<int:pk>/
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]