from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
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


class PostListView(ListView):
    """Display all blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class PostDetailView(DetailView):
    """Display a single blog post"""
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allow authenticated users to create new posts"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow post authors to edit their posts"""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow post authors to delete their posts"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts/'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author