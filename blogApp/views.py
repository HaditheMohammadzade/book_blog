from django.shortcuts import render
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from multiprocessing import context
from pdb import post_mortem
from re import A
from urllib import request
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404 , redirect
from django.http import Http404, HttpResponseRedirect , HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import TemplateView , ListView , DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from .models import Post 
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
from django.contrib.auth import login , logout
from . import models
# from .filters import PostsFilter
# from .forms import CommentForm


class HomePageView(TemplateView):
    template_name = 'home.html'

def signupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request,'signup.html',{'form' :form})


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request,'login.html',{'form' :form})

def logoutView(request):
    logout(request)
    return redirect('home')

class createPostSuperUserView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Post
    template_name = 'newPost.html'
    fields = ['title','text','image']
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class editPostSuperUserView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Post
    template_name = 'editPost.html'
    fields = ['title','text']
    
class PostDetailView(DetailView):
    model = Post
    count_hit = True
    template_name = 'postDetail.html'


