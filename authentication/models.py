from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password, phone, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        if not username:
            raise ValueError('The username must be set')
        if username.strip() == 'string':
            raise ValueError('The username must be set')
        if not phone:
            raise ValueError('The phone number must be set')
        if not password:
            raise ValueError('The password must be set')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        if not username:
            raise ValueError('The username must be set')
        if username.strip().lower() == 'string':
            raise ValueError('The username must be set')
        if not password:
            raise ValueError('The password must be set')
        user = self.create_user(username, email, password, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    phone = models.CharField(unique=True, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]
    objects = UserManager()

    def __str__(self):
        return f'{self.username}'

    def token(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            "access_token": str(refresh_token.access_token),
            "refresh_token": str(refresh_token)
        }