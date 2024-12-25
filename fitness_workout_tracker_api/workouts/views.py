from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Workout, Exercise, WorkoutExercise
from .serializers import (
    WorkoutSerializer, 
    ExerciseSerializer, 
    WorkoutExerciseSerializer,
    AddExerciseToWorkoutSerializer
)

class ExerciseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing exercises
    """
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Exercise.objects.filter(user=self.request.user)

class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workouts
    """
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AddExerciseToWorkoutSerializer
        return WorkoutExerciseSerializer

    def get_queryset(self):
        return WorkoutExercise.objects.filter(
            workout_id=self.kwargs['workout_pk'],
            workout__user=self.request.user
        )

    def create(self, request, workout_pk=None):
        """
        Add an existing exercise to the workout
        """
        workout = get_object_or_404(Workout, id=workout_pk, user=request.user)
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            exercise = Exercise.objects.get(id=serializer.validated_data['exercise_id'])
            workout_exercise = WorkoutExercise.objects.create(
                workout=workout,
                exercise=exercise,
                sets=serializer.validated_data['sets'],
                reps=serializer.validated_data['reps'],
                weight=serializer.validated_data.get('weight'),
                notes=serializer.validated_data.get('notes', ''),
                order=serializer.validated_data.get('order', 0)
            )
            return Response(
                WorkoutExerciseSerializer(workout_exercise).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, workout_pk=None, pk=None):
        """
        Update an exercise in the workout
        """
        workout_exercise = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            exercise = Exercise.objects.get(id=serializer.validated_data['exercise_id'])
            workout_exercise.exercise = exercise
            workout_exercise.sets = serializer.validated_data['sets']
            workout_exercise.reps = serializer.validated_data['reps']
            workout_exercise.weight = serializer.validated_data.get('weight')
            workout_exercise.notes = serializer.validated_data.get('notes', '')
            workout_exercise.order = serializer.validated_data.get('order', 0)
            workout_exercise.save()
            
            return Response(
                WorkoutExerciseSerializer(workout_exercise).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, workout_pk=None, pk=None):
        """
        Remove an exercise from the workout
        """
        workout_exercise = get_object_or_404(
            WorkoutExercise,
            workout_id=workout_pk,
            id=pk,
            workout__user=request.user
        )
        workout_exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
