from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_id_id = models.CharField(max_length=255)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""

# Create your models here.
class Poll(models.Model):
    poll_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.poll_name

    def get_absolute_url(self):
        return reverse('poll:poll-detail', kwargs={'pk': self.pk})

    def get_answered_url(self):
        return reverse('poll:passed-questions', kwargs={'pk': self.pk})


class Question(models.Model):
    question_type_choices = (
        ('T', 'Text answer'),
        ('CO', 'Choose one'),
        ('CM', 'Choose many')
    )
    question_text = models.TextField()
    question_type = models.CharField(choices=question_type_choices,
                                     max_length=2)
    belong_to_poll = models.ForeignKey(Poll, on_delete=models.CASCADE,
                                       default=0, related_name='questions')

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('poll:question-detail', kwargs={'pk': self.pk})


class Choice(models.Model):
    choice_text = models.TextField()
    belong_to_question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # def get_queryset(self):
    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    answer_text = models.TextField()
    answer_by_user = models.CharField(max_length=255)

    question_type = models.CharField(max_length=2, default=0)
    answer_to_poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    answer_to_question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text
