from service import config
from service.config import get_db_url

DB_CONFIG = {
    "connections": {
        "default": get_db_url(
            config.DB_PROV,
            config.DB_USER,
            str(config.DB_PSWD),
            config.DB_SERV,
            config.DB_PORT,
            config.DB_NAME,
        ),
    },
    "apps": {"models": {"models": ["service.models"]}},
}
