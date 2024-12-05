from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from myapp.models import Publication
from users.models import CustomUser, Follow


class UserSignUpView(TemplateView):
    template_name = 'sign_up.html'


class UserMakeSignUpView(View):

    def post(self, request, *args, **kwargs):
        data = request.POST

        password = data['password']

        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        user = CustomUser.objects.create_user(
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        login(request, user)
        return render(request, 'home.html')



class LoginPageView(TemplateView):
    template_name = 'login.html'


class UserMakeLoginView(View):

    def post(self, request, *args, **kwargs):
        data = request.POST
        username = data['username']
        password = data['password']

        user = CustomUser.objects.get(username=username)
        print('пользователь ', user)

        correct = user.check_password(password)
        print('коррект равен ', correct)

        if correct == True:
            login(request, user)
            return render(request, 'home.html', context={'logged_in': True})
        else:
            return render(request, 'login.html', context={'logged_in': False})


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        current_user = self.request.user

        followers_count = current_user.my_follower.all().count()
        following_count = current_user.my_following.all().count()

        publication_count = Publication.objects.filter(user=current_user).count()

        context = {
            'publications': Publication.objects.all(),
            'publication_count': publication_count,
            'current_user': current_user,
            'following_count': following_count,
            'follower_count': followers_count
        }
        return context


def follow_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        if not user_id:
            return HttpResponse("User ID is missing.", status=400)

        target_user = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user

        if target_user != current_user:
            if target_user.followers.filter(id=current_user.id).exists():
                # Удаление подписки
                target_user.followers.remove(current_user)
            else:
                # Добавление подписки
                target_user.followers.add(current_user)

        # Перенаправление на страницу профиля
        return redirect(target_user.get_absolute_url())

    return HttpResponse("Invalid request.", status=400)

















