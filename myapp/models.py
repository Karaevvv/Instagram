from django.db import models
from users.models import CustomUser


class Publication(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        default=True,
        related_name='my_publications')

    image = models.ImageField(upload_to='publications/')
    description = models.TextField(blank=True)
    create_date = models.DateField(auto_now_add=True)

    likes = models.ManyToManyField(CustomUser)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return f"Publication by {self.user.username}"

    class Meta:
        verbose_name_plural = 'Публикации'
        verbose_name = 'Публикация'


class Comment(models.Model):

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='publication_comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comments')
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

    def __str__(self) -> str:
        return f'{self.user.username} commented on {self.publication}'


