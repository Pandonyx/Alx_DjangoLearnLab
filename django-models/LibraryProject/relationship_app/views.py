# relationship_app/views.py
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

from .models import Book
from .models import Library   # <- explicit Library import required

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view using DetailView
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# Registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

# Login and logout will use Django’s built-in class-based views
class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"

class CustomLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"