import re
from django.core.cache import cache
from .models import Post
from .serializers import PostSerializer
from app.permissions import IsAuthorOrReadOnly
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        return Response({
            'post': self.get_serializer(post).data,
            'likes_count': post.likes.count(),
        })
        
class LikePostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'status': 'Disliked post'})
        else:
            post.likes.add(user)
            return Response({'status': 'Liked post'})
        
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserFeedView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        cache_key = f'user_feed_{user.id}'
        feed = cache.get(cache_key)
        if feed is None:
            feed = Post.objects.filter(author__in=user.following.all()).order_by('-created_at')
            cache.set(cache_key, feed, 60 * 15)
        return feed

class HashtagSearchView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()

        if not query:
            return Post.objects.none()

        all_posts = Post.objects.all()
        filtered_posts = [post for post in all_posts if f'{query}' in post.hashtags]

        return filtered_posts
