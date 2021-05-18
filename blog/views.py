from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, 
                                DetailView, 
                                CreateView, 
                                UpdateView, 
                                DeleteView)
from .models import Post
from django.contrib.auth.models import User

# Home page
class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

# Detailed blog post
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

# Create new blog post
class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    fields = ['title', 'content']
    context_object_name = 'post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update a blog post
class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin ,UpdateView):
    model = Post
    fields = ['title', 'content']
    context_object_name = 'post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        
        return False

# Delete a blog post
class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
                return True 
            
        return False

# View a particular user's posts
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# About page 
def about(request):
    return render(request, 'blog/about.html')

