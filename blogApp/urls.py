from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.createPostSuperUserView.as_view(), name='post_create'),
    path('signup/', views.signupView, name='signup'),
    path('login/', views.loginView, name = 'login'),
    path('logout/', views.logoutView, name = 'logout'),
    path("",views.HomeView,name='home'),
    path("<int:pk>/edit/",views.editPostSuperUserView.as_view(),name='post_edit'),
    path("<int:pk>/",views.PostDetailView.as_view(),name='post_detail'),
    path("archive/",views.PostList,name='archive'),


]
