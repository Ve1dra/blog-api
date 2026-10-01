from email.policy import default

from django.db import models
from authentication.models import User
import uuid

# Create your models here.
class Posts(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    heading = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='user_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)