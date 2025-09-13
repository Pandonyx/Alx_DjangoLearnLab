from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Book, CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "first_name", "last_name", "date_of_birth", "profile_photo")

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_year']

class ExampleForm(forms.Form):
    """A simple example form for demonstration purposes."""
    name = forms.CharField(max_length=100, help_text="Enter your full name.")
    email = forms.EmailField(help_text="Enter a valid email address.")