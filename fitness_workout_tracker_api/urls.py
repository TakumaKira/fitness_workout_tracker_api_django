from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from fitness_workout_tracker_api.authentication.views import AuthViewSet
from fitness_workout_tracker_api.workouts.views import WorkoutViewSet, ExerciseViewSet, WorkoutExerciseViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'exercises', ExerciseViewSet, basename='exercise')

# Create a nested router for workout exercises
workouts_router = NestedDefaultRouter(router, r'workouts', lookup='workout')
workouts_router.register(r'exercises', WorkoutExerciseViewSet, basename='workout-exercises')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(workouts_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]