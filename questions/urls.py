from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from .views import View

urlpatterns = [
    path('proba/', QuestionsViewList.as_view()),
    # path('',  HomeListView.as_view(), name='home'),
    path('', QuestionsViews, name='questions'),
    path('edit_questions/', edit_questions, name='edit_questions'),
    path('edit_question/<int:pk>/', question_detail, name='question_detail_url'),
    path('login/', login, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('questionajax/', question_ajax, name='questionajax'),
    path('nextquestion/', next_question, name='nextquestion'),
    path('statistics/', statistics, name='statistics'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
