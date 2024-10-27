from django.urls import path
from . import views

urlpatterns = [
    path('users/register/', views.RegisterView.as_view(), name='user_register'),
    path('users/follow/<str:username>/', views.FollowUserView.as_view(), name='follow_user'),
    path('users/unfollow/<str:username>/', views.UnfollowUserView.as_view(), name='unfollow_user'),
    path('users/<str:username>/', views.UserDetailView.as_view(), name='user_detail')
]
