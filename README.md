To setup the project, run the following commands:

```bash
python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows
pip install -r requirements.txt
```

And whenever you install any new packages, run the following command to update the requirements.txt file:

```bash
pip freeze > requirements.txt
```

Setup the database in this order:

```bash
# First, create migration files if you have changes on custom models
python manage.py makemigrations

# Then, apply migrations to the database
python manage.py migrate

# Finally, create an admin user
python manage.py createsuperuser --username admin --email admin@example.com
```

To run the project, use the following command:

```bash
python manage.py runserver
```

To run security checks, use the following command:

```bash
DJANGO_DEBUG=False python manage.py check --deploy
```

## Running Tests

Run all tests:
```bash
python manage.py test
```

Run tests for a specific app:
```bash
python manage.py test fitness_workout_tracker_api.workouts.tests
```

Run a specific test class:
```bash
python manage.py test fitness_workout_tracker_api.workouts.tests.WorkoutIsolationTests
```

Run a specific test method:
```bash
python manage.py test fitness_workout_tracker_api.workouts.tests.WorkoutIsolationTests.test_exercise_isolation
```

Run a specific test method:
```bash
python manage.py test fitness_workout_tracker_api.workouts.tests.WorkoutIsolationTests.test_exercise_isolation
```

To run tests with more detailed output:
```bash
python manage.py test -v 2
```
