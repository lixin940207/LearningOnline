"""LearningOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from LearningOnline.settings import MEDIA_ROOT
from apps.operations.views import IndexView
from apps.users.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # configure access url for uploading images
    url('media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # url('static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    url('org/', include(('apps.organizations.urls', "organizations"), namespace="org")),
    url('course/', include(('apps.courses.urls', "courses"), namespace="course")),
    url('op/', include(('apps.operations.urls', "operations"), namespace="op")),
    url('users/', include(('apps.users.urls', "users"), namespace="users")),


]
