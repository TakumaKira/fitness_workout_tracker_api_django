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

You need to setup the database:

```bash
python manage.py migrate
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
