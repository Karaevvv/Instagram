from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):

    avatar = models.ImageField(upload_to='avatars/', blank=True)
    profile_description = models.TextField(default=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('profile-url', kwargs={'username': self.username})


class Follow(models.Model):

    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='my_follower')

    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='my_following')

    created_at = models.DateTimeField(auto_now_add=True)


