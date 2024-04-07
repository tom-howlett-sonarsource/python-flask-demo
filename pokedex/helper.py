import re
import sqlite3

from pokedex.utils import is_pikachu


class ConnectionWrapper:
    """A simple connection wrapper class"""

    def __init__(self, db_path):
        self.__conn = sqlite3.connect(db_path)

    def get_single_pokemon(self, pokemon_id):
        statement = f"SELECT * FROM POKEDEX WHERE id = '{pokemon_id}'"
        return self.__conn.execute(statement).fetchone()

    def get_all_pokemons(self):
        statement = "SELECT * FROM POKEDEX"
        return self.__conn.execute(statement).fetchall()

    def register_subscriber(self, email):
        try:
            self.__conn.execute("INSERT into SUBSCRIBERS(email) values (?)", (email,))
            self.__conn.commit()
        except sqlite3.DatabaseError:
            raise Exception("Problem with the database!")
        except sqlite3.IntegrityError:
            raise ValueError("Email already exists!")

    def cleanup(self, should_close: bool):
        if should_close:
            self.__conn.close()


def fetch_all_pokemons(wrapper: ConnectionWrapper):
    return wrapper.get_all_pokemons()

#add a method call fetch_pokemon_by_name that accepts a name and returns the pokemon with that name
def fetch_pokemon_by_name(wrapper: ConnectionWrapper, pokemon_name: str):
    statement = f"SELECT * FROM POKEDEX WHERE name = '{pokemon_name}'"
    result = wrapper.__conn.execute(statement).fetchone()
    if result is None:
        raise ValueError("Pokemon not found")
    return result

#add a method call fetch_pokemon_by_start that accepts a letter and returns all the pokemon whose name starts with that letter
def fetch_pokemon_by_start(wrapper: ConnectionWrapper, start_letter: str):
    statement = f"SELECT * FROM POKEDEX WHERE name LIKE '{start_letter}%'"
    return wrapper.__conn.execute(statement).fetchall()

#add a method to prefix a pokemon name with a given string and return the new name
def prefix_pokemon_name(name: str, prefix: str):
    return prefix + name


def register_subscriber(wrapper: ConnectionWrapper, email):
    pattern = re.compile(r"(.*)@(.*\..*)")
    if not pattern.match(email):
        ValueError("Invalid email!")
    wrapper.register_subscriber(email)
    pass


def fetch_pokemon(wrapper: ConnectionWrapper, pokemon_id: str):
    result = wrapper.get_single_pokemon(pokemon_id)
    if result is None:
        raise "Pokemon not found"
    if pokemon_id == 25:
        if is_pikachu(result):
            # Team Rocket is trying to steal Pikachu (#25)!
            result = ("", "We stole Pikachu!", "", "")
    return result
