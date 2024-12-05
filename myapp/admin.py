from django.contrib import admin

from myapp.models import Publication, Comment


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('create_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_at',)
