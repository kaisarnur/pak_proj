# Generated by Django 4.2 on 2023-04-22 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Habit title')),
                ('description', models.TextField(verbose_name='Description')),
                ('number_of_repeats', models.IntegerField(verbose_name='Number of repeats')),
                ('execution_frequency', models.CharField(choices=[('day', 'day'), ('week', 'week'), ('month', 'month')], max_length=10, verbose_name='Execution frequency')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
