import requests
import threading
import json

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
NUM_THREADS = 5
TOTAL_POKEMON = 100

# Diccionario para traducir los tipos de inglés a español
type_translation = {
    "normal": "Normal",
    "fire": "Fuego",
    "water": "Agua",
    "grass": "Planta",
    "electric": "Eléctrico",
    "ice": "Hielo",
    "fighting": "Lucha",
    "poison": "Veneno",
    "ground": "Tierra",
    "flying": "Volador",
    "psychic": "Psíquico",
    "bug": "Bicho",
    "rock": "Roca",
    "ghost": "Fantasma",
    "dragon": "Dragón",
    "dark": "Siniestro",
    "steel": "Acero",
    "fairy": "Hada"
}

# Función para obtener datos de un Pokémon
def get_pokemon_data(start_id, end_id, thread_counter):
    for index, pokemon_id in enumerate(range(start_id, end_id + 1), start=1):
        try:
            response = requests.get(f"{BASE_URL}{pokemon_id}")
            response.raise_for_status()  # Verifica errores HTTP
            data = response.json()
            
            # Extrae la información necesaria
            name = data['name']
            types = [type_translation.get(t['type']['name'], t['type']['name'].capitalize()) for t in data['types']]
            stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

            # Contador de Pokémon
            pokemon_number = (thread_counter - 1) * (TOTAL_POKEMON // NUM_THREADS) + index
            print(f"Número de Pokédex: {pokemon_number}")

            # Formatea la salida
            print(f"Nombre: {name.capitalize()}")
            if len(types) == 2:
                print(f"Tipos: {types[0]} y {types[1]}")
            else:
                print(f"Tipo: {types[0]}")

            print("Estadísticas:")
            print(f"  HP: {stats.get('hp', 'N/A')}")
            print(f"  Ataque: {stats.get('attack', 'N/A')}")
            print(f"  Defensa: {stats.get('defense', 'N/A')}")
            print(f"  Ataque especial: {stats.get('special-attack', 'N/A')}")
            print(f"  Defensa especial: {stats.get('special-defense', 'N/A')}")
            print(f"  Velocidad: {stats.get('speed', 'N/A')}")
            print("\n" + "-" * 30 + "\n")
        
        except requests.RequestException as e:
            print(f"Error fetching data for Pokémon ID {pokemon_id}: {e}")

if __name__ == "__main__":
    threads = []
    pokemons_per_thread = TOTAL_POKEMON // NUM_THREADS

    for i in range(NUM_THREADS):
        start_id = i * pokemons_per_thread + 1
        end_id = start_id + pokemons_per_thread - 1
        thread = threading.Thread(target=get_pokemon_data, args=(start_id, end_id, i + 1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
