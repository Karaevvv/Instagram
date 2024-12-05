"""
URL configuration for instagram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp.views import HomeView, toggle_like, CreateNewPostView, CommentView
from users.views import UserMakeSignUpView, UserSignUpView, UserMakeLoginView, \
    LoginPageView, ProfileView, follow_user

urlpatterns = [
    path('admin/', admin.site.urls),

    path('home/', HomeView.as_view(), name='home-url'),

    path('registration/', UserSignUpView.as_view(), name='registration-url'),
    path('make-registration/', UserMakeSignUpView.as_view(), name='make-signup-url'),

    path('login/', LoginPageView.as_view(), name='login-url'),
    path('make-login/', UserMakeLoginView.as_view(), name='make-login-url'),

    path('create_comments/', CommentView.as_view(), name='create-comment-url'),

    path('profile/', ProfileView.as_view(), name='profile-url'),
    path('follow/', follow_user, name='follow-user'),

    path('create-new-post/', CreateNewPostView.as_view(), name='create-new-post-url'),

    path('like/<int:publication_id>/', toggle_like, name='toggle-like')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
