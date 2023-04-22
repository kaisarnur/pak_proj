from django.db import models

from accounts.models import User


class Habit(models.Model):
    EXECUTION_FREQUENCY_CHOICE = [('day', 'day'), ('week', 'week'), ('month', 'month')]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='habits', verbose_name='User')
    title = models.CharField(max_length=150, verbose_name='Habit title')
    description = models.TextField(verbose_name='Description')
    number_of_repeats = models.IntegerField(verbose_name='Number of repeats')
    execution_frequency = models.CharField(
        choices=EXECUTION_FREQUENCY_CHOICE, max_length=10, verbose_name='Execution frequency')
    start_date = models.DateField(verbose_name='Start date')
    end_date = models.DateField(verbose_name='End date')

    def __str__(self):
        return f'{self.user.email}: {self.title}'
