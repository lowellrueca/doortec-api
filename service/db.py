import random
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

AERICH_CONFIG = {
    "connections": {
        "default": get_db_url(
            config.DB_PROV,
            config.DB_USER,
            str(config.DB_PSWD),
            config.DB_HOST,
            config.DB_PORT,
            config.DB_NAME,
        ),
    },
    "apps": {"models": {"models": ["service.models", "aerich.models"]}},
}

async def seed_data():
    from service.models import Door
    
    models = await Door.all()
    random_series = ["maine", "iowa", "prague", "florence", "lucerne", "zurich", "bruges", "stockholm", "nuremberg", "viena", "edinburgh", "venice", "amsterdam"]
    random_prices = [2000.00, 2250.00, 3350.00, 4250.00, 5700.00, 7370.00, 8000.00, 9050.00]
    mock_products = [Door(series=random.choice(random_series), price=random.choice(random_prices)) for i in range(300) if len(models) == 0]
    await Door.bulk_create(mock_products)

