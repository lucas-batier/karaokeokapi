"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views

from backend.settings import MEDIA_URL, MEDIA_ROOT
from karaokeok import views

router = routers.DefaultRouter()
router.register(r'songs', views.SongView, 'song')
router.register(r'artists', views.ArtistView, 'artist')
router.register(r'users', views.UserView, 'user')

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', authtoken_views.obtain_auth_token),
    path('api/register/', views.RegisterView.as_view()),
    path('api/current_user/', views.RetrieveCurrentUserView.as_view()),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
