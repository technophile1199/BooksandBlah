from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
# Importing default ListView inorder to perform operations of update and delete on POsts
from django.views.generic import (
	ListView, 
	DetailView,
 	CreateView,
	UpdateView,
	DeleteView
	)
from .models import Post

# Create your views here.


def home(request):
	
	return render(request, "blog/home.html", {'posts':Post.objects.all(), 'title':'Home Page'})
	


def about(request):
	return render(request, "blog/about.html", {'title':'About Page'})
	
	
	
def year(request, year):
	return HttpResponse(f"<h1> {year}</h1>")


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 3

# class which displays posts of specific user only
class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Post.objects.filter(author = user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post

#Class to create a post by user
#Mixin Validates login and redirects to login if not logged in
class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	fields = ['title', 'content']

	#Setting author to current logged in profile
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	#Setting author to current logged in profile
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url ='/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False