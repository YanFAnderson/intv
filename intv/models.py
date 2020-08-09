from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=120, blank=False, null=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    description = models.CharField(max_length=255, blank=True, null=False)


class Question(models.Model):
    text = models.CharField(max_length=255, null=False)
    type_choices = [
        ('TEXT', 'Text'),
        ('YN', 'Yes/No'),
        ('VALUES', 'With values')
    ]
    type = models.CharField(max_length=55, choices=type_choices, default='TEXT', null=False, blank=False)
    poll_id = models.IntegerField(null=False, blank=False)
    # Я бы хотел сделать массив, но подключать Постгрес слишком долго
    values = models.CharField(max_length=255, blank=True, null=True)


class Answer(models.Model):
    question_id = models.IntegerField(null=False, blank=False)
    answer = models.CharField(max_length=255, null=False, blank=False)
    user_id = models.IntegerField(null=False, blank=False)
