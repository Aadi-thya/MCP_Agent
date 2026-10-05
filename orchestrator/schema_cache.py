import json
from pathlib import Path


CACHE_FILE = Path(__file__).parent / "schema_cache.json"


def get_schema_from_cache():

    if not CACHE_FILE.exists():
        return None

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return None


def save_schema_to_cache(schema):

    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as file:
            json.dump(schema, file, indent=4)

    except OSError as e:
        print(f"Could not save schema cache: {e}")


def clear_schema_cache():

    if CACHE_FILE.exists():
        CACHE_FILE.unlink()

        print("Schema cache cleared.")