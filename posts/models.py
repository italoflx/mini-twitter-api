from django.db import models
from users.models import User

class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    title = models.TextField()
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    hashtags = models.CharField(max_length=30,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}..."
