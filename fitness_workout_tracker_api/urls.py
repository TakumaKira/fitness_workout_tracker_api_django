from django.urls import include, path
from rest_framework import routers
from fitness_workout_tracker_api.authentication.views import AuthViewSet
from fitness_workout_tracker_api.workouts.views import WorkoutViewSet

router = routers.DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'workouts', WorkoutViewSet, basename='workout')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]