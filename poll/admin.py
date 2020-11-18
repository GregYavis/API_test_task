from django.contrib import admin

from .models import Poll, Question, Choice,Answer


# Register your models here.
class ChoisePollQuestions(admin.TabularInline):
    model = Question
    extra = 3


class PollAdmin(admin.ModelAdmin):
    exclude = ("start_date ",)
    fieldsets = [(None, {'fields': ['poll_name']}),
                 ('Start_date', {'fields': ['start_date']}),
                 ('End date', {'fields': ['end_date']}),
                 ('Description', {'fields': ['description']})]
    inlines = [ChoisePollQuestions]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['start_date']
        else:
            return []


class AnswerQuestion(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerQuestion]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Answer)
