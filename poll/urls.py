from django.contrib import admin
from django.urls import path, include
from .views import PollsView, PollDetail, QuestionDetail, UserPassedPolls, UserAnsweredPollQuestions

app_name = 'poll'
urlpatterns = [
    path('', PollsView.as_view(), name='polls-list'),
    path('poll/<int:pk>', PollDetail.as_view(), name='poll-detail'),
    path('question/<int:pk>', QuestionDetail.as_view(),
         name='question-detail'),
    path('answered_polls/', UserPassedPolls.as_view(), name='passed-polls'),
    path('answered_poll_questions/<int:pk>',
         UserAnsweredPollQuestions.as_view(), name='passed-questions')

]
