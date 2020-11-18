from django.contrib import admin
from django.urls import path, include
from .views import PollsView, PollDetail, QuestionDetail, UserPassedPolls, \
    UserAnsweredPollQuestions, ApiPollsView, ApiQuestionsView, \
    ApiChoiceForQuestion

app_name = 'poll'
urlpatterns = [
    path('', PollsView.as_view(), name='polls-list'),
    path('poll/<int:pk>', PollDetail.as_view(), name='poll-detail'),
    path('question/<int:pk>', QuestionDetail.as_view(),
         name='question-detail'),
    path('answered_polls/', UserPassedPolls.as_view(), name='passed-polls'),
    path('answered_poll_questions/<int:pk>',
         UserAnsweredPollQuestions.as_view(), name='passed-questions'),
    path('api/', ApiPollsView.as_view()),
    path('api/<int:pk>', ApiPollsView.as_view()),
    path('api/questions/', ApiQuestionsView.as_view()),
    path('api/questions/<int:pk>', ApiQuestionsView.as_view()),
    path('api/questions/choices/<int:pk>', ApiChoiceForQuestion.as_view()),
    path('api/questions/choices/option/<int:pk>',ApiChoiceForQuestion.as_view()),

]
