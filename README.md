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
