from django.shortcuts import render
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from multiprocessing import context
from pdb import post_mortem
from re import A
from urllib import request
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404 , redirect
from django.http import Http404, HttpResponseRedirect , HttpResponseNotAllowed , HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import TemplateView , ListView , DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from .models import Post, Comment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
from django.contrib.auth import login , logout
from . import models
# from .filters import PostsFilter
# from .forms import CommentForm
from .forms import CommentForm
from .filters import PostsFilter

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
    fields = ['title','text','image', 'category']
    
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        # slug = self.kwargs["slug"]

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk)
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, email=email, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


def HomeView(request):
    posts = models.Post.objects.all().order_by('-publishDate')
    post_list = Post.objects.all()
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filter = PostsFilter(request.GET, queryset=posts)
    posts = filter.qs
    args = {'posts' :posts, 'filter' :filter, 'page_obj' :page_obj, 'posts' :post_list}
    return render(request, 'home.html',args)
    


def PostList(request):
    posts = models.Post.objects.all().order_by('-publishDate')
    post_list = Post.objects.all()
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filter = PostsFilter(request.GET, queryset=posts)
    posts = filter.qs
    args = {'posts' :posts, 'filter' :filter, 'page_obj' :page_obj, 'posts' :post_list}
    return render(request, 'archive.html',args)
    
def rate(request: HttpRequest, post_id: int, rating: int) -> HttpResponse:
    post = Post.objects.get(id=post_id)
    Rating.objects.filter(post=post, user=request.user).delete()
    post.rating_set.create(user=request.user, rating=rating)
    return HomeView(request)