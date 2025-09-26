from __future__ import annotations

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify

class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str | None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

def _generate_public_slug(base: str | None = None) -> str:
    # Random slug generator - kewl
    rand = get_random_string(6, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789")
    if base:
        base = slugify(base)
        return f"{base}-{rand}"
    return rand

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=150, blank=True)
    public_slug = models.SlugField(max_length=32, unique=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']

    def __str__(self) -> str: # Useful in admin and shell idk why copilot says that
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.public_slug:
            base = self.display_name or (self.email.split("@")[0] if self.email else None)
            slug = _generate_public_slug(base)
            # Make sure the slug is unique
            Model = type(self)
            while Model.objects.filter(public_slug=slug).exists():
                slug = _generate_public_slug(base)
            self.public_slug = slug
        super().save(*args, **kwargs)
    
    @property
    def public_path(self) -> str:
        # For public routes type "/<slug/>"
        return f"/{self.public_slug}/"