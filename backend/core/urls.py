# core/urls.py
from django.urls import path
from .views import RegisterView, LoginView, BlogPostView

from rest_framework_simplejwt.views import TokenRefreshView
from .views import blog_posts

urlpatterns = [
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/posts/', BlogPostView.as_view()),
    path('api/blog-posts/', blog_posts, name='blog_posts'),
]