from os import path
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from starlette.config import Config


env_file = path.abspath(".env")
config = Config(env_file=env_file)

DB_PROV = config(key="DB_PROV", cast=str, default="sqlite")
DB_USER = config(key="DB_USER", cast=str, default="user")
DB_PSWD = config(key="DB_PSWD", cast=Secret, default="1234")
DB_HOST = config(key="DB_HOST", cast=str, default="localhost")
DB_SERV = config(key="DB_SERV", cast=str, default="localhost")
DB_PORT = config(key="DB_PORT", cast=int, default=5678)
DB_NAME = config(key="DB_NAME", cast=str, default="db")
DEBUG = config(key="DEBUG", cast=bool, default=False)
HOST = config(key="HOST", cast=CommaSeparatedStrings, default="localhost")
PORT = config(key="PORT", cast=int, default=5000)


def get_db_url(
    provider: str, user: str, password: str, host: str, port: int, db_name: str
) -> str:
    return f"{provider}://{user}:{password}@{host}:{port}/{db_name}"
