from django.urls import path
from . import views
from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    register,
    CustomLoginView,
    CustomLogoutView,
)

urlpatterns = [
    path("books/", views.list_books, name="list_books"),  # function-based view
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),  # class-based view
    
    # Authentication URLs
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
]