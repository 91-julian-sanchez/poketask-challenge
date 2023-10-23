# REQUISITOS
Docker:
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```

# Crear un usuario admin 
```python
from django.contrib.auth.models import User

# Crear un nuevo usuario
user = User.objects.create_user('admin', password='****password****')
```
# crear token de usuario admin
```
python manage.py drf_create_token admin
```

# migrations commands
```bash
python manage.py makemigrations
python manage.py migrate
```
# RUN PROJECT
## run server
```bash
python manage.py runserver
```

## run worker with celery
Linux
```bash
celery -A core worker -l info
```
Windows
```bash
celery -A core worker --pool=solo -l info
```

## Send task to broker from django shell
```python
from poketasks.tasks import fetch_and_create_pokemon
fetch_and_create_pokemon.delay()
```

Run flower
```bash
celery -A poketasks_project flower --port=5001
```

crear token de usuario admin
python manage.py drf_create_token admin