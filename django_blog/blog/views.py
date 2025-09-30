from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post


def home(request):
    """View for displaying all blog posts"""
    posts = Post.objects.all().order_by('-published_date')
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    """View for the about page"""
    return render(request, 'blog/about.html', {'title': 'About'})