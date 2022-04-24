"""s3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from drive.views import UserAvatarUpload
from drive.views import login,signup,get_file
from rest_framework.authtoken import views
from django.urls import include
from .router import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/upload",UserAvatarUpload.as_view(),name="test"),
    path("api/login",login,name="login"),
    path("api/signup",signup,name="signup"),
    path("api/getfiles",get_file,name="get files"),

]
