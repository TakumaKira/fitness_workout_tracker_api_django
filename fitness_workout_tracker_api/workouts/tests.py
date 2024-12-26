from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Exercise, Workout, WorkoutExercise, Comment
from datetime import date

class WorkoutIsolationTests(TestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password123')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password123')
        
        # Create API clients
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.client1.force_authenticate(user=self.user1)
        self.client2.force_authenticate(user=self.user2)

        # Create test data for user1
        self.exercise1 = Exercise.objects.create(
            user=self.user1,
            name='Push-ups',
            description='Basic push-ups'
        )
        
        self.workout1 = Workout.objects.create(
            user=self.user1,
            title='Morning Workout',
            date=date.today(),
            duration=30
        )

        self.workout_exercise1 = WorkoutExercise.objects.create(
            workout=self.workout1,
            exercise=self.exercise1,
            sets=3,
            reps=10
        )

        self.comment1 = Comment.objects.create(
            workout=self.workout1,
            user=self.user1,
            text='Great workout!'
        )

    def test_exercise_isolation(self):
        """Test that users can't access each other's exercises"""
        # Try to get another user's exercise
        response = self.client2.get(f'/exercises/{self.exercise1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to update another user's exercise
        response = self.client2.put(
            f'/exercises/{self.exercise1.id}/',
            {'name': 'Modified Push-ups', 'description': 'Modified'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to delete another user's exercise
        response = self.client2.delete(f'/exercises/{self.exercise1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify exercise remains unchanged
        self.exercise1.refresh_from_db()
        self.assertEqual(self.exercise1.name, 'Push-ups')

    def test_workout_isolation(self):
        """Test that users can't access each other's workouts"""
        # Try to get another user's workout
        response = self.client2.get(f'/workouts/{self.workout1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to update another user's workout
        response = self.client2.put(
            f'/workouts/{self.workout1.id}/',
            {
                'title': 'Modified Workout',
                'date': date.today().isoformat(),
                'duration': 45
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to delete another user's workout
        response = self.client2.delete(f'/workouts/{self.workout1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify workout remains unchanged
        self.workout1.refresh_from_db()
        self.assertEqual(self.workout1.title, 'Morning Workout')

    def test_workout_exercise_isolation(self):
        """Test that users can't modify workout exercises of other users"""
        # Try to get another user's workout exercises
        response = self.client2.get(f'/workouts/{self.workout1.id}/exercises/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to add exercise to another user's workout
        response = self.client2.post(
            f'/workouts/{self.workout1.id}/exercises/',
            {
                'exercise_id': self.exercise1.id,
                'sets': 4,
                'reps': 12
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to modify another user's workout exercise
        response = self.client2.put(
            f'/workouts/{self.workout1.id}/exercises/{self.workout_exercise1.id}/',
            {
                'exercise_id': self.exercise1.id,
                'sets': 5,
                'reps': 15
            }
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify workout exercise remains unchanged
        self.workout_exercise1.refresh_from_db()
        self.assertEqual(self.workout_exercise1.sets, 3)
        self.assertEqual(self.workout_exercise1.reps, 10)

    def test_comment_isolation(self):
        """Test that users can't modify comments on other users' workouts"""
        # Try to get comments from another user's workout
        response = self.client2.get(f'/workouts/{self.workout1.id}/comments/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to add comment to another user's workout
        response = self.client2.post(
            f'/workouts/{self.workout1.id}/comments/',
            {'text': 'Unauthorized comment'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to modify another user's comment
        response = self.client2.put(
            f'/workouts/{self.workout1.id}/comments/{self.comment1.id}/',
            {'text': 'Modified comment'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify comment remains unchanged
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.text, 'Great workout!')

    def test_list_isolation(self):
        """Test that list endpoints only return user's own data"""
        # Test exercises list
        response = self.client2.get('/exercises/')
        self.assertEqual(len(response.data), 0)  # user2 should see no exercises

        # Test workouts list
        response = self.client2.get('/workouts/')
        self.assertEqual(len(response.data), 0)  # user2 should see no workouts

        # Verify user1 sees their data
        response = self.client1.get('/exercises/')
        self.assertEqual(len(response.data), 1)  # user1 should see their exercise

        response = self.client1.get('/workouts/')
        self.assertEqual(len(response.data), 1)  # user1 should see their workout
