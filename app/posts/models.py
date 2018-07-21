from django.conf import settings
from django.db import models


class Post(models.Model):
    auth = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
