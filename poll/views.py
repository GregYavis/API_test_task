from django.shortcuts import render, get_object_or_404, redirect
from .models import Choice, Poll, Question, Answer
from django.views.generic import ListView, DetailView, View, FormView
from .forms import ChoiseManyForm, ChooseOneForm, TextInputForm
import json


# Create your views here.

class PollsView(ListView):
    model = Poll
    template_name = 'poll/homepage.html'
    context_object_name = 'polls'


class PollDetail(DetailView):
    model = Poll
    template_name = 'poll/poll.html'
    context_object_name = 'questions'


class QuestionDetail(View):
    model = Question
    template_name = 'poll/question.html'
    context_object_name = 'question'

    def get(self, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs.get('pk'))
        # get question type
        type_of_question = question.question_type
        if type_of_question == 'CM':
            options = question.choice_set.all().values_list('choice_text',
                                                            flat=True)
            form = ChoiseManyForm(choices_options=options)
            context = {'form': form}
            return render(self.request, 'poll/question.html', context)
        elif type_of_question == 'CO':
            options = question.choice_set.all().values_list('choice_text',
                                                            flat=True)
            form = ChooseOneForm(choices_options=options)
            context = {'form': form}
            return render(self.request, 'poll/question.html', context)
            # next get question options string
        elif type_of_question == 'T':
            form = TextInputForm()
            context = {'form': form}
            # text = q_type.
            return render(self.request, 'poll/question.html', context)

    def post(self, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs.get('pk'))
        print(question.belong_to_poll)
        question_type = question.question_type
        selected = self.request.POST.getlist('form')
        user_answer = Answer(answer_to_poll=question.belong_to_poll,
                             answer_to_question=question,
                             answer_text=selected,
                             answer_by_user=self.request.user,
                             question_type=question_type,
                             )
        user_answer.save()

        return redirect('poll:polls-list')


class UserPassedPolls(View):

    def get(self, *args, **kwargs):
        users_answered_polls = Answer.objects.filter(answer_by_user=
                                                     self.request.user)

        query_data = [{'poll': answer['answer_to_poll_id'],
                       'question': answer['answer_to_question_id'],
                       'answers': answer['answer_text']} for answer in
                      users_answered_polls.values()]
        # for i in data:
        #    print(i)

        user_polls = set(i['poll'] for i in query_data)
        # user_questions = set(i['question'] for i in data)

        return_data = [Poll.objects.get(pk=poll) for poll in user_polls]
        # print(return_data)
        context = {'answered': return_data}
        return render(self.request, 'poll/user_answered.html', context)


class UserAnsweredPollQuestions(View):
    def get(self, *args, **kwargs):
        users_answered_polls = Answer.objects.filter(answer_by_user=
                                                     self.request.user)
        all_polls = Question.objects.all()
        question_ids = set([answer['id'] for answer in all_polls.values() if
                            answer['belong_to_poll_id'] == self.kwargs.get(
                                'pk')])

        questions = [Question.objects.get(pk=question_id) for question_id
                     in question_ids]

        data = [{'poll': answer['answer_to_poll_id'],
                 'question': answer['answer_to_question_id'],
                 'answers': answer['answer_text']} for answer in
                users_answered_polls.values() if answer['answer_to_poll_id']
                == self.kwargs.get('pk')]
        usr_answered_questions = set(i['question'] for i in data)

        return_data = [Question.objects.get(pk=question_id) for question_id
                       in usr_answered_questions]
        print(questions)
        print(return_data)
        unanswered_questions = question_ids - usr_answered_questions
        unanswered_questions = [Question.objects.get(pk=question_id) for
                                question_id in unanswered_questions]
        context = {'questions': return_data,
                   'unanswered': unanswered_questions}
        return render(self.request, 'poll/poll_question_answered.html',
                      context)
