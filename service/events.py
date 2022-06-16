from tortoise import Tortoise
from service.db import DB_CONFIG


async def on_startup():
    from service.db import seed_data

    await Tortoise.init(config=DB_CONFIG)
    await Tortoise.generate_schemas()
    await seed_data()


async def on_shutdown():
    await Tortoise.close_connections()
