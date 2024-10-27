from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    path('posts/search/', views.HashtagSearchView.as_view(), name='post_search'),
    path('feed/', views.UserFeedView.as_view(), name='user_feed'),
]
