"""oprosnik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from .views import redirect_question

urlpatterns = [
    # path('', views.home, name='home'),
    # path('', views.HomeListView.as_view(), name='home'),
    # path('signup/', views.signup, name='signup'),
    # path('questions/', views.questions, name='questions'),
    # path('questions2/', views.QuestionsViews.as_view(), name='questions2'),
    # path('accounts/', include('django.contrib.auth.urls')),
    #path('', redirect_question),
    path('', include("questions.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    # path('', include("questions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
