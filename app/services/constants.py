import pathlib

BASE_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent.parent
PATH_ENV_FILE: pathlib.Path = BASE_DIR / ".env"

MAX_LENGTH: int = 125
MIN_LENGTH: int = 3
