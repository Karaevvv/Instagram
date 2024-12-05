
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
import json

from myapp.forms import CommentForm
from myapp.models import Publication, Comment
from users.models import CustomUser


class PublicationView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):

        context = {
            'publications': Publication.objects.all()
        }
        return context


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user

        publications = Publication.objects.filter(user__in=current_user.following.all()).union(
            Publication.objects.filter(user=current_user)
        ).order_by('-create_date')

        other_users = CustomUser.objects.exclude(id=current_user.id)

        following_users = current_user.following.all()

        recommendations = CustomUser.objects.exclude(id__in=following_users).exclude(id=current_user.id)



        context = {
            'publications_list': Publication.objects.all(),
            'current_user': current_user,
            'publications': publications,
            'other_users': other_users,
            'following_users': following_users,
            'comment_form': CommentForm(),
            'recommendations': recommendations,
        }
        return context


def toggle_like(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    user = request.user

    if user in publication.likes.all():
        publication.likes.remove(user)  # Удалить лайк
    else:
        publication.likes.add(user)  # Добавить лайк

    return redirect('home-url')  # Перенаправление на ту же страницу


class CommentView(View):
    def post(self, request, *args, **kwargs):
        publication_id = request.POST.get('publication_id')
        text = request.POST.get('text')

        if not publication_id:
            return HttpResponse('Поле publication_id отсутствует или пусто', status=400)

        if not text:
            return HttpResponse('Поле комментария (text) пусто', status=400)

        try:
            publication = Publication.objects.get(id=publication_id)
        except (Publication.DoesNotExist, ValueError):
            return HttpResponse('Публикация не найдена или id некорректен', status=404)

        # Создание комментария
        Comment.objects.create(user=request.user, publication=publication, text=text)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CreateNewPostView(View):

    def post(self, request, *args, **kwargs):
        current_user = self.request.user  # получаем пользователя который хочет загрузить публикацию

        data = request.POST
        files = request.FILES

        Publication.objects.create(
            image=files['image-upload'],
            user=current_user,
            description=data['description']
        )
        return redirect('home-url')









