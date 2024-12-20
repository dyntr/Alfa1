import os
from dotenv import load_dotenv

# -------------------------------
# Načtení proměnných z .env souboru
# -------------------------------

load_dotenv()


# -------------------------------
# Funkce pro bezpečné načítání environmentálních proměnných
# -------------------------------

def get_env_variable(var_name, default=None, required=True, cast_type=str):
    """
    Načte environmentální proměnnou s validací a volitelným převodem typu.

    Args:
        var_name (str): Název environmentální proměnné.
        default (any): Výchozí hodnota, pokud není proměnná definována (volitelné).
        required (bool): Určuje, zda je proměnná povinná (výchozí True).
        cast_type (type): Typ, na který má být hodnota převedena (výchozí str).

    Returns:
        any: Hodnota proměnné převedená na zadaný typ.

    Raises:
        ValueError: Pokud je proměnná povinná a chybí, nebo má nesprávný formát.
    """
    # Načtení hodnoty z prostředí nebo výchozí hodnoty
    value = os.getenv(var_name, default)

    # Kontrola, zda je proměnná povinná
    if value is None and required:
        raise ValueError(f"Chybí povinná environmentální proměnná: '{var_name}'.")

    # Pokus o převod hodnoty na požadovaný typ
    try:
        return cast_type(value)
    except (ValueError, TypeError):
        raise ValueError(
            f"Proměnná '{var_name}' má nesprávný formát. Očekává se typ {cast_type.__name__}."
        )


# -------------------------------
# Načítání proměnných s validací a bezpečností
# -------------------------------

# Discord API konfigurace
DISCORD_TOKEN = get_env_variable("DISCORD_TOKEN", required=True)
UPLOAD_CHANNEL_ID = get_env_variable("UPLOAD_CHANNEL_ID", required=True, cast_type=int)
DISCORD_UPLOAD_LIMIT = get_env_variable("DISCORD_UPLOAD_LIMIT", default=25 * 1024 * 1024, cast_type=int)

# Cesty a složky
TEMP_FOLDER = get_env_variable("TEMP_FOLDER", default="temp", cast_type=str)
LOG_FOLDER = get_env_variable("LOG_FOLDER", default="logs", cast_type=str)
SPLIT_FOLDER = get_env_variable("SPLIT_FOLDER", default="split_files", cast_type=str)
DOWNLOAD_FOLDER = get_env_variable("DOWNLOAD_FOLDER", default="downloads", cast_type=str)

# -------------------------------
# Zajištění existence potřebných složek
# -------------------------------

def ensure_directory_exists(directory):
    """
    Zkontroluje, zda složka existuje, a pokud ne, vytvoří ji.

    Args:
        directory (str): Cesta ke složce.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Složka '{directory}' byla vytvořena.")


# Kontrola a vytvoření složek
for folder in [TEMP_FOLDER, LOG_FOLDER, SPLIT_FOLDER, DOWNLOAD_FOLDER]:
    ensure_directory_exists(folder)


# -------------------------------
# Výpis konfigurace pro ověření
# -------------------------------

def print_config():
    """
    Vypíše aktuální konfiguraci pro ladění.
    """
    print(f"DISCORD_TOKEN: {'***' if DISCORD_TOKEN else 'Not Set'}")
    print(f"UPLOAD_CHANNEL_ID: {UPLOAD_CHANNEL_ID}")
    print(f"DISCORD_UPLOAD_LIMIT: {DISCORD_UPLOAD_LIMIT / (1024 * 1024)} MB")
    print(f"TEMP_FOLDER: {TEMP_FOLDER}")
    print(f"LOG_FOLDER: {LOG_FOLDER}")
    print(f"SPLIT_FOLDER: {SPLIT_FOLDER}")
    print(f"DOWNLOAD_FOLDER: {DOWNLOAD_FOLDER}")


# Volitelné: Vypíše konfiguraci při spuštění
if __name__ == "__main__":
    print_config()
