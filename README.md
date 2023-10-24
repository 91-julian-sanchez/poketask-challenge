Crea una aplicación Django simple llamada "Poketasks". Debe incluir un modelo de datos "Pokemon" que tenga campos como "nombre", "id" , "habilidades" y los que consideres relevantes. Configura una vista que permita a los usuarios listar, buscar y agregar habilidades al pokemon.


Crea un api usando django rest framework que permita crear y buscar pokemon usando el api. Genera un swagger para documentar este endpoint. Genera un método de autenticación para estos endpoints


Usando Celery crea una tarea que extraiga cada 35 segundos un pokemon aleatorio usando el siguiente api: https://pokeapi.co/ , luego de extraerlo envíalo usando un request http al api que creaste en el paso anterior.


Condiciones:

no pueden insertarse pokemon repetidos . si el pokemon ya existe debe descartarse y traer otro. 


Luego de que se ejecuta la tarea, usando django signals se debe enviar una notificación al correo indicando cual pokemon se creó mediante la tarea de celery. si la tarea trae un pokemon repetido debe guardarse en un log con sus atributos.

# REQUIREMENTS
Install and run Rabbitmq
Docker:
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```
## Install requirements
```
pip install -r requirements.txt
```

Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Create an admin user
```python
from django.contrib.auth.models import User
user = User.objects.create_user('admin', password='****password****')
```
## Create admin user token
```
python manage.py drf_create_token admin
```

## Enviroments
Create an **.env** file and set up the project variables you can see an example in **.env.example**

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
### Create pokemon
```curl
curl --location '{BASE_URL}/poketasks/pokemons/' \
--header 'Authorization: token {AUTH_TOKEN}' \
--header 'Content-Type: application/json' \
--data '{
    "name": "{POKEMON_NAME}",
    "id": {POKEMON_ID},
    "skills": "{POKEMON_SKILLS}"
}'
```
### Get pokemon
```curl
curl --location '{BASE_URL}/poketasks/pokemons/{POKEMON_ID}/' \
--header 'Authorization: token {AUTH_TOKEN}'
```

### Add pokemon skills
```curl
curl --location '{BASE_URL}/poketasks/pokemons/{POKEMON_ID}/add_skill/' \
--header 'Authorization: token {AUTH_TOKEN}' \
--header 'Content-Type: application/json' \
--data '{
    "new_skill": "{SKILLS}"
}'
```

### Get all pokemons
```curl
curl --location '{BASE_URL}/poketasks/pokemons/' \
--header 'Authorization: token {AUTH_TOKEN}'
```

## API docs
see {BASE_URL}/swagger/ or {BASE_URL}/redoc/ 

```
 (\__/)
  (o^.^)
z(_(")(")
```