"""intv URL Configuration

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
from django.contrib import admin
from django.urls import path

from .views import PollListView, PollAddView, PollEditView, PollDeleteView, QuestionListView, QuestionAddView, \
    QuestionEditView, QuestionDeleteView, PollsGetView, AnswerAddView, AnswerListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/poll/list', PollListView.as_view()),
    path('api/poll/add', PollAddView.as_view()),
    path('api/poll/edit', PollEditView.as_view()),
    path('api/poll/delete', PollDeleteView.as_view()),
    path('api/question/list', QuestionListView.as_view()),
    path('api/question/add', QuestionAddView.as_view()),
    path('api/question/edit', QuestionEditView.as_view()),
    path('api/question/delete', QuestionDeleteView.as_view()),
    path('api/polls/get', PollsGetView.as_view()),
    path('api/answer/add', AnswerAddView.as_view()),
    path('api/answer/list', AnswerListView.as_view()),
]
