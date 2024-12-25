from rest_framework import serializers
from .models import Workout, Exercise, WorkoutExercise, Comment

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'exercise_name', 'sets', 'reps', 'weight', 'notes', 'order']

class AddExerciseToWorkoutSerializer(serializers.ModelSerializer):
    exercise_id = serializers.IntegerField()

    class Meta:
        model = WorkoutExercise
        fields = ['exercise_id', 'sets', 'reps', 'weight', 'notes', 'order']

    def validate_exercise_id(self, value):
        try:
            exercise = Exercise.objects.get(
                id=value,
                user=self.context['request'].user
            )
            return value
        except Exercise.DoesNotExist:
            raise serializers.ValidationError("Exercise not found")

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'username', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(source='workout_exercises', many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'title', 'description', 'date', 'duration', 
                 'created_at', 'updated_at', 'exercises', 'comments']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 