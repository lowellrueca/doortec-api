from tortoise import Tortoise
from service.db import DB_CONFIG


async def on_startup():
    await Tortoise.init(config=DB_CONFIG)
    await Tortoise.generate_schemas()

    # models: List[Door] = await Door.all()
    # seed random data
    # random_names = ["orange", "lemon", "banana", "grapes", "cherry", "avocado", "berry"]
    # mock_products: List[Door] = [Product(name=random.choice(random_names)) for i in range(24) if len(models) == 0]
    # await Door.bulk_create(mock_products)


async def on_shutdown():
    await Tortoise.close_connections()
