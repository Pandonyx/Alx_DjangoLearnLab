from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .models import Book
from .forms import BookForm, CustomUserCreationForm, ExampleForm

# --- Book CRUD Views ---
@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """Displays a list of all books."""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    """Handles creation of a new book."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list') # Assumes a URL name 'book_list'
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_update(request, pk):
    """Handles updating an existing book."""
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, pk):
    """Handles deletion of a book."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'object': book})

# --- Authentication Views ---

def register(request):
    """Handles user registration using the custom user model."""
    if request.method == "POST":
        # request.FILES is needed for the profile_photo
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in directly after registration
            return redirect("book_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "bookshelf/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "bookshelf/login.html"


class CustomLogoutView(LogoutView):
    template_name = "bookshelf/logout.html"
