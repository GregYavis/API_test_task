import datetime
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status

from .models import Choice, Poll, Question, Answer
from django.views.generic import ListView, DetailView, View, FormView
from .forms import ChoiseManyForm, ChooseOneForm, TextInputForm
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PollSerializer, \
    QuestionSerializer, ChoiceSerializer


# Create your views here.
class ApiPollsView(APIView):
    def get(self, request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response({'polls': serializer.data})

    def post(self, request):

        poll = request.data.get('polls')
        serializer = PollSerializer(data=poll)
        if serializer.is_valid(raise_exception=True):
            poll_saved = serializer.save()
        return Response({'success': f'Poll {poll_saved.poll_name} created '
                                    f'with primary key {poll_saved.pk}'})

    def put(self, request, pk):

        existing_poll = get_object_or_404(Poll.objects.all(),
                                          pk=pk)

        data = request.data.get('polls')
        serializer = PollSerializer(instance=existing_poll, data=data,
                                    partial=True)
        if serializer.is_valid(raise_exception=True):
            poll_saved = serializer.save()
        return Response({'success': f'Poll updated {poll_saved.pk}'})

    def delete(self, request, pk):
        existing_poll = get_object_or_404(Poll.objects.all(), pk=pk)
        existing_poll.delete()
        return Response({'mesage': f'Poll with id {pk} has been deleted'},
                        status=204)


class ApiQuestionsView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response({'questions': serializer.data})

    def post(self, request):
        question = request.data.get('questions')
        serializer = QuestionSerializer(data=question)
        if serializer.is_valid(raise_exception=True):
            question_saved = serializer.save()
        return Response({'success': f'Question created with primary key '
                                    f'{question_saved.pk}'})

    def put(self, request, pk):
        existing_question = get_object_or_404(Question.objects.all(), pk=pk)
        data = request.data.get('questions')
        serializer = QuestionSerializer(instance=existing_question, data=data,
                                        partial=True)
        if serializer.is_valid(raise_exception=True):
            question_saved = serializer.save()
        return Response({'sucess': f'Question updated {question_saved.pk}'})

    def delete(self, request, pk):
        existing_poll = get_object_or_404(Question.objects.all(), pk=pk)
        existing_poll.delete()
        return Response({'mesage': f'Poll with id {pk} has been deleted'},
                        status=204)


class ApiChoiceForQuestion(APIView):
    def get(self, request, **kwargs):
        choices = Choice.objects.filter(belong_to_question=
                                        self.kwargs.get('pk'))
        serializer = ChoiceSerializer(choices, many=True)
        return Response({'choices': serializer.data})

    def post(self, request, pk):
        choice_to_add = request.data.get('choices')

        question = Question.objects.get(pk=choice_to_add['belong_to_question'])

        if str(question.question_type) == 'T':
            return Response(data='Question type requires only text '
                                 'answers',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ChoiceSerializer(data=choice_to_add)
            if serializer.is_valid(raise_exception=True):
                choice_saved = serializer.save()
                return Response({'sucess': 'Option to question saved'})

    def put(self, request, pk):
        existing_choice = get_object_or_404(Choice.objects.all(), pk=pk)
        if str(existing_choice.belong_to_question.question_type) == "T":
            return Response(data='Question type requires only text '
                                 'answers and didnt support choices',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data.get('choices')
            serializer = ChoiceSerializer(instance=existing_choice, data=data,
                                          partial=True)
            if serializer.is_valid(raise_exception=True):
                choice_saved = serializer.save()
            return Response({'success': 'Choice to question was updated'})

    def delete(self, request, pk):
        existing_poll = get_object_or_404(Choice.objects.all(), pk=pk)
        print(existing_poll)
        existing_poll.delete()
        return Response({'mesage': f'Poll with id {pk} has been deleted'},
                        status=204)


class PollsView(ListView):
    def get(self, *args, **kwargs):
        polls = Poll.objects.all()
        actual_polls = [poll for poll in polls if poll.end_date
                        >= datetime.datetime.now().date()]
        context = {'polls': actual_polls}
        return render(self.request, 'poll/homepage.html', context)


class PollDetail(DetailView):
    model = Poll
    template_name = 'poll/poll.html'
    context_object_name = 'questions'

    def get(self, *args, **kwargs):
        poll_questions = Question.objects.filter(
            belong_to_poll=self.kwargs.get('pk'))

        context = {'questions': poll_questions}
        return render(self.request, 'poll/poll.html', context)


class QuestionDetail(View):
    model = Question
    template_name = 'poll/question.html'
    context_object_name = 'question'

    def get(self, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs.get('pk'))
        # get question type
        type_of_question = question.question_type
        if type_of_question == 'CM':
            options = question.choice_set.all().values_list(
                'choice_text',
                flat=True)
            form = ChoiseManyForm(choices_options=options)
            context = {'form': form}
            return render(self.request, 'poll/question.html', context)
        elif type_of_question == 'CO':
            options = question.choice_set.all().values_list(
                'choice_text',
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
        if not self.request.user.is_authenticated:
            if not self.request.session or not self.request.session.session_key:
                self.request.session.save()
            question = Question.objects.get(pk=self.kwargs.get('pk'))
            question_type = question.question_type
            selected = self.request.POST.getlist('form')
            user_answer = Answer(
                answer_to_poll=question.belong_to_poll,
                answer_to_question=question,
                answer_text=selected,
                answer_by_user=self.request.session.session_key,
                question_type=question_type,
            )
            user_answer.save()

            return redirect('poll:polls-list')
        else:
            question = Question.objects.get(pk=self.kwargs.get('pk'))
            question_type = question.question_type
            selected = self.request.POST.getlist('form')
            user_answer = Answer(
                answer_to_poll=question.belong_to_poll,
                answer_to_question=question,
                answer_text=selected,
                answer_by_user=self.request.user,
                question_type=question_type,
            )
            user_answer.save()
            return redirect('poll:polls-list')


class UserPassedPolls(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            users_answered_polls = Answer.objects.filter(
                answer_by_user=
                self.request.session.session_key)

            query_data = [{'poll': answer['answer_to_poll_id'],
                           'question': answer['answer_to_question_id'],
                           'answers': answer['answer_text']} for answer
                          in
                          users_answered_polls.values()]

            user_polls = set(i['poll'] for i in query_data)

            return_data = [Poll.objects.get(pk=poll) for poll in
                           user_polls]

            context = {'answered': return_data}
            return render(self.request, 'poll/user_answered.html',
                          context)
        else:
            users_answered_polls = Answer.objects.filter(
                answer_by_user=
                self.request.user)

            query_data = [{'poll': answer['answer_to_poll_id'],
                           'question': answer['answer_to_question_id'],
                           'answers': answer['answer_text']} for answer
                          in
                          users_answered_polls.values()]

            user_polls = set(i['poll'] for i in query_data)

            return_data = [Poll.objects.get(pk=poll) for poll in
                           user_polls]

            context = {'answered': return_data}
            return render(self.request, 'poll/user_answered.html',
                          context)


class UserAnsweredPollQuestions(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            users_answered_polls = Answer.objects.filter(
                answer_by_user=
                self.request.session.session_key)
            all_polls = Question.objects.all()
            question_ids = set(
                [answer['id'] for answer in all_polls.values() if
                 answer['belong_to_poll_id'] == self.kwargs.get(
                     'pk')])
            data = [{'poll': answer['answer_to_poll_id'],
                     'question': answer['answer_to_question_id'],
                     'answers': answer['answer_text']} for answer in
                    users_answered_polls.values() if
                    answer['answer_to_poll_id']
                    == self.kwargs.get('pk')]
            usr_answered_questions = set(i['question'] for i in data)

            return_data = [Question.objects.get(pk=question_id) for
                           question_id
                           in usr_answered_questions]

            unanswered_questions = question_ids - usr_answered_questions
            unanswered_questions = [
                Question.objects.get(pk=question_id)
                for
                question_id in unanswered_questions]
            context = {'questions': return_data,
                       'unanswered': unanswered_questions}
            return render(self.request,
                          'poll/poll_question_answered.html',
                          context)
        else:
            users_answered_polls = Answer.objects.filter(
                answer_by_user=
                self.request.user)
            all_polls = Question.objects.all()
            question_ids = set(
                [answer['id'] for answer in all_polls.values() if
                 answer['belong_to_poll_id'] == self.kwargs.get(
                     'pk')])

            data = [{'poll': answer['answer_to_poll_id'],
                     'question': answer['answer_to_question_id'],
                     'answers': answer['answer_text']} for answer in
                    users_answered_polls.values() if
                    answer['answer_to_poll_id']
                    == self.kwargs.get('pk')]
            usr_answered_questions = set(i['question'] for i in data)

            return_data = [Question.objects.get(pk=question_id) for
                           question_id
                           in usr_answered_questions]

            unanswered_questions = question_ids - usr_answered_questions
            unanswered_questions = [
                Question.objects.get(pk=question_id)
                for
                question_id in unanswered_questions]
            context = {'questions': return_data,
                       'unanswered': unanswered_questions}
            return render(self.request,
                          'poll/poll_question_answered.html',
                          context)
