from datetime import date

from django.db import models


class CompanyDetails(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_xp = models.IntegerField(default=0)
    charity = models.CharField(max_length=10, default='')

    class Meta:
        verbose_name = 'Company details'
        verbose_name_plural = 'Company details'
        ordering = ['company_id']


class UserDetails(models.Model):
    user_sub = models.CharField(max_length=70, primary_key=True)
    user_name = models.CharField(max_length=30)
    company_id = models.IntegerField()
    start_date = models.DateField(default=date.today())
    user_xp = models.IntegerField(default=0)
    user_level = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'User details'
        verbose_name_plural = 'User details'


class TaskProgress(models.Model):
    user_sub = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='tasks')
    task_id = models.CharField(max_length=10)
    completed = models.BooleanField(default=False)
    partial = models.CharField(max_length=40, default='', blank=True)

    class Meta:
        verbose_name = 'Task progress'
        verbose_name_plural = 'Task progress'

        ordering = ['task_id']


class UserFeedback(models.Model):
    task_id = models.CharField(max_length=10)
    company_id = models.IntegerField()
    answer0 = models.CharField(max_length=2, blank=True)
    answer1 = models.CharField(max_length=2, blank=True)
    answer2 = models.CharField(max_length=2, blank=True)
    answer3 = models.CharField(max_length=2, blank=True)
    answer4 = models.CharField(max_length=2, blank=True)
    answer5 = models.CharField(max_length=2, blank=True)
    answer6 = models.CharField(max_length=2, blank=True)
    answer7 = models.CharField(max_length=2, blank=True)
    answer8 = models.CharField(max_length=2, blank=True)
    answer9 = models.CharField(max_length=2, blank=True)

    class Meta:
        verbose_name = 'User feedback'
        verbose_name_plural = 'User feedback'


# Create your models here.
