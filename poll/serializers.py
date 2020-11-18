from rest_framework import serializers
from .models import Poll, Question, Choice


class PollSerializer(serializers.ModelSerializer):
    questions = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Poll

        fields = ['pk', 'poll_name', 'start_date', 'end_date', 'description',
                  'questions']

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.poll_name = validated_data.get('poll_name',
                                                instance.poll_name)
        instance.start_date = validated_data.get('start_date',
                                                 instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.save()

        return instance


class QuestionSerializer(serializers.ModelSerializer):
    question_type = serializers.ChoiceField(
        choices=Question.question_type_choices)
    question_text = serializers.CharField()

    class Meta:
        model = Question

        fields = ['question_text', 'question_type', 'belong_to_poll']

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.question_text = validated_data.get('question_text',
                                                    instance.question_text)
        instance.question_type = validated_data.get('question_type',
                                                    instance.question_type)
        instance.belong_to_poll = validated_data.get('belong_to_poll',
                                                     instance.belong_to_poll)
        instance.save()
        return instance


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text', 'belong_to_question']

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.choice_text = validated_data.get('choice_text',
                                                  instance.choice_text)
        instance.belong_to_question = validated_data.get('belong_to_question',
                                                         instance.belong_to_question)
        instance.save()
        return instance


"""
            poll_name = serializers.CharField(max_length=255)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    description = serializers.CharField()
    """
