import requests
from celery import shared_task
from time import sleep
import random

BASE_URL = 'http://localhost:8000/poketasks/pokemons/'
POKEMON_API_URL = 'https://pokeapi.co/api/v2/pokemon/'
ADMIN_TOKEN = "28b2ef74ce819726fe7586b94af5360115dee3fa"
MAX_RETRIES = 5  # Número máximo de reintentos permitidos

# Function to fetch Pokemon data from the external API
def fetch_pokemon(pokemon_id):
    """
    Fetches Pokemon data from the external API.
    """
    url = f'{POKEMON_API_URL}{pokemon_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error while fetching data from the {url}: {e}')
        return None

# Function to extract Pokemon abilities
def extract_abilities(pokemon_data):
    """
    Extracts Pokemon abilities from the obtained data.
    """
    try:
        abilities = [item['ability']['name'] for item in pokemon_data['abilities']]
        return ', '.join(abilities)
    except (KeyError, TypeError) as e:
        print(f'Error while extracting abilities: {e}')
        return ''

# Function to send Pokemon data to the local API
def request_create_pokemon(pokemon_data):
    """
    Sends Pokemon data to the local API for creation.
    """
    try:
        headers = {
            'Authorization': f'token {ADMIN_TOKEN}'
        }

        response = requests.post(BASE_URL, json=pokemon_data, headers=headers)
        return response
    except Exception as e:
        print(f'Error while sending data to the API: {e}', e)
        return None

# Function to create a Pokemon with circuit breaker
def create_pokemon(pokemon_data, retries=0):
    if retries >= MAX_RETRIES:
        print(f"->> The {MAX_RETRIES} retries have been exceeded. The Pokemon cannot be created.")
        raise Exception(f"The {MAX_RETRIES} retries have been exceeded. The Pokemon cannot be created.")

    abilities = extract_abilities(pokemon_data)
    response = request_create_pokemon({
        "name": pokemon_data.get("name"),
        "pokemon_id": pokemon_data.get("id"),
        "skills": abilities
    })

    response_data = response.json()

    if response.status_code == 201:
        print("Pokemon created successfully", response_data)
        return response_data
    elif response.status_code == 400 and response_data.get("error") == 'DUP_ENTRY':
        print("Duplicate Pokemon", response_data.get('existing_pokemon'))
        # Circuit breaker - Trying a limited number of retries
        # while retries < MAX_RETRIES:
        #     new_pokemon_data = fetch_pokemon(random.randint(1, 3))
        #     if new_pokemon_data and new_pokemon_data.get('id') != pokemon_data.get('id'):
        #         create_pokemon(new_pokemon_data, retries + 1)
        #         break
        #     retries += 1
    else:
        print(f"Failed to create the Pokemon. Status code: {response.status_code }")

    return response_data

# Scheduled task to fetch and create Pokemon periodically
@shared_task
def fetch_and_create_pokemon():
    """
    Main function to fetch and create Pokemon periodically.
    """
    # while True:
    try:
        pokemon_data = fetch_pokemon(random.randint(1, 15))
        if pokemon_data:
            return create_pokemon(pokemon_data)
    except Exception as e:
        print(f'Unexpected error: {e}')
    sleep(10)
    return None
