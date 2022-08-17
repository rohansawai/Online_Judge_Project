from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import *


urlpatterns = [
    path('', views.indexView, name="home"),
    path('dashboard/', views.dashboardView, name="dashboard"),      
    path('login/', LoginView.as_view(next_page='dashboard'), name="login_url"),
    path('register/',views.registerView, name="register_url"),
    path('logout/', LogoutView.as_view(next_page='dashboard'), name="logout"),
    path('<int:problem_id>/', views.details, name = 'details'),
    path('<int:problem_id>/submit/', views.submission, name='submission'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]   