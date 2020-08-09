from rest_framework import serializers

from .models import Poll, Question, Answer


class PollSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=120, allow_null=False, allow_blank=False)
    start_date = serializers.DateField(allow_null=False)
    end_date = serializers.DateField(allow_null=False)
    description = serializers.CharField(max_length=255, allow_null=False, allow_blank=True)

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    text = serializers.CharField(max_length=255, allow_null=False, allow_blank=True)
    type_choices = [
        ('TEXT', 'Text'),
        ('YN', 'Yes/No'),
        ('VALUES', 'With values')
    ]
    type = serializers.ChoiceField(choices=type_choices, allow_null=False, allow_blank=False)
    poll_id = serializers.IntegerField(allow_null=False)
    values = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.type = validated_data.get("type", instance.type)
        instance.poll_id = validated_data.get("poll_id", instance.poll_id)
        instance.values = validated_data.get("values", instance.values)
        instance.save()
        return instance


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    question_id = serializers.IntegerField(allow_null=False)
    answer = serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    user_id = serializers.IntegerField(allow_null=False)

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)
