from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from . import models
from . import serializers
from . import tasks

class RegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True) 
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user_to_follow = get_object_or_404(models.User, username=username)

        if user_to_follow == request.user:
            return Response({"error": "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if user_to_follow in request.user.following.all():
            return Response({"error": f"You are already following {user_to_follow.username}."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        
        tasks.send_follow_notification.delay(
            follower_username=request.user.username,
            followed_username=user_to_follow.username,
            followed_email=user_to_follow.email
        )

        return Response({"message": f"You started following {user_to_follow.username}"}, status=status.HTTP_200_OK)

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user_to_unfollow = get_object_or_404(models.User, username=username)

        if request.user == user_to_unfollow:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.following.filter(id=user_to_unfollow.id).exists():
            request.user.following.remove(user_to_unfollow)
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
        