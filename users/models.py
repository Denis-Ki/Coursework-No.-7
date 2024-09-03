from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# Create your models here.
class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email address")
    phone_number = models.CharField(
        max_length=35, verbose_name="Phone number", blank=True, null=True
    )
    tg_name = models.CharField(
        max_length=50, verbose_name="Telegram username", help_text="Введите Telegram User ID"
    )
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Avatar", blank=True, null=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"Email: {self.email} Tg name: {self.tg_name}"
