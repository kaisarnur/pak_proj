from rest_framework import serializers

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'title', 'description', 'number_of_repeats',
            'execution_frequency', 'start_date', 'end_date'
        ]

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     habit = Habit.objects.create(**validated_data)
    #     return habit